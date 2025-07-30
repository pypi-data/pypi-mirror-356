"""
同步二进制大对象服务
"""
from pathlib import Path
from typing import Optional, Union, BinaryIO, Iterator

from .base_file_service import BaseFileService
from ...enums import UploadMode
from ...errors import ValidationError
from ...rpc import SyncGrpcClient
from ...schemas import FileUploadResponse, UploadUrlResponse
from ...utils import HttpUploader, HttpDownloader, retry_with_backoff, get_file_mime_type


class SyncBlobService(BaseFileService):
    """同步文件（二进制大对象）服务"""

    def __init__(self, client: SyncGrpcClient):
        """
        初始化文件（二进制大对象）服务

        Args:
            client: 同步gRPC客户端
        """
        self.client = client
        self.http_uploader = HttpUploader()
        self.http_downloader = HttpDownloader()

    def _generate_resumable_upload_url(
            self,
            file_name: str,
            file_size: int,
            folder_id: Optional[str] = None,
            file_type: str = "file",
            mime_type: str = None,
            file_hash: str = None,
            is_temporary: Optional[bool] = False,
            expire_seconds: Optional[int] = None,
            **metadata
    ) -> UploadUrlResponse:
        """
        生成断点续传URL

        Args:
            file_name: 文件名
            file_size: 文件大小
            folder_id: 文件夹ID
            file_type: 文件类型
            mime_type: MIME类型
            file_hash: 文件哈希
            is_temporary: 是否为临时文件
            expire_seconds: 过期秒数
            **metadata: 额外的元数据（如 x-org-id, x-user-id 等）

        Returns:
            上传URL响应
        """
        from ...rpc.gen import file_service_pb2, file_service_pb2_grpc

        stub = self.client.get_stub(file_service_pb2_grpc.FileServiceStub)

        request = file_service_pb2.UploadUrlRequest(
            file_name=file_name,
            file_size=file_size,
            file_type=file_type,
            mime_type=mime_type or "application/octet-stream",
            file_hash=file_hash,
            is_temporary=is_temporary,
            expire_seconds=expire_seconds if is_temporary and expire_seconds else None,
        )

        if folder_id:
            request.folder_id = folder_id

        # 构建元数据
        grpc_metadata = self.client.build_metadata(**metadata)

        response = stub.GenerateResumableUploadUrl(request, metadata=grpc_metadata)

        return UploadUrlResponse(
            file=self._convert_file_info(response.file),
            upload_file=self._convert_upload_file_info(response.upload_file),
            upload_url=response.url
        )

    def _confirm_upload_completed(self, file_id: str, **metadata) -> None:
        """
        确认上传完成

        Args:
            file_id: 文件ID
            **metadata: 额外的元数据（如 x-org-id, x-user-id 等）
        """
        from ...rpc.gen import file_service_pb2, file_service_pb2_grpc

        stub = self.client.get_stub(file_service_pb2_grpc.FileServiceStub)

        request = file_service_pb2.UploadCompletedRequest(file_id=file_id)

        # 构建元数据
        grpc_metadata = self.client.build_metadata(**metadata)

        stub.ConfirmUploadCompleted(request, metadata=grpc_metadata)

    @retry_with_backoff(max_retries=3)
    def _upload_file(
            self,
            file_name: str,
            content: Union[bytes, BinaryIO, Path],
            folder_id: Optional[str] = None,
            file_type: str = "file",
            mime_type: Optional[str] = None,
            is_temporary: Optional[bool] = False,
            expire_seconds: Optional[int] = None,
            **metadata
    ) -> FileUploadResponse:
        """
        直接上传文件

        Args:
            file_name: 文件名
            content: 文件内容（字节、文件对象或路径）
            folder_id: 文件夹ID
            file_type: 文件类型
            mime_type: MIME类型
            is_temporary: 是否为临时文件
            expire_seconds: 过期秒数
            **metadata: 额外的元数据（如 x-org-id, x-user-id 等）

        Returns:
            文件信息
        """
        from ...rpc.gen import file_service_pb2, file_service_pb2_grpc

        stub = self.client.get_stub(file_service_pb2_grpc.FileServiceStub)

        # 处理不同类型的内容
        if isinstance(content, Path):
            if not content.exists():
                raise ValidationError(f"文件不存在: {content}")
            with open(content, "rb") as f:
                file_bytes = f.read()
            if not mime_type:
                mime_type = get_file_mime_type(content)
        elif isinstance(content, bytes):
            file_bytes = content
        elif hasattr(content, 'read'):
            file_bytes = content.read()
        else:
            raise ValidationError("不支持的内容类型")

        # 构建请求
        request = file_service_pb2.UploadFileRequest(
            file_name=file_name,
            content=file_bytes,
            file_type=file_type,
            mime_type=mime_type or "application/octet-stream",
            is_temporary=is_temporary,
            expire_seconds=expire_seconds,
        )

        if folder_id:
            request.folder_id = folder_id

        # 构建元数据
        grpc_metadata = self.client.build_metadata(**metadata)

        # 发送请求
        response = stub.UploadFile(request, metadata=grpc_metadata)

        # 转换响应
        return FileUploadResponse(
            file=self._convert_file_info(response.file),
            upload_file=self._convert_upload_file_info(response.upload_file),
        )

    def _upload_stream(
            self,
            file_name: str,
            content: Union[bytes, BinaryIO, Path],
            file_size: int,
            folder_id: Optional[str],
            file_type: str,
            mime_type: str,
            file_hash: str,
            is_temporary: Optional[bool] = False,
            expire_seconds: Optional[int] = None,
            **metadata
    ) -> FileUploadResponse:
        """客户端直传实现"""
        # 获取上传URL，以及对应的文件和上传文件信息
        upload_url_resp = self.generate_upload_url(
            file_name=file_name,
            file_size=file_size,
            folder_id=folder_id,
            file_type=file_type,
            mime_type=mime_type,
            file_hash=file_hash,
            is_temporary=is_temporary,
            expire_seconds=expire_seconds if is_temporary and expire_seconds else None,
            **metadata
        )

        # 上传文件到对象存储
        self.http_uploader.upload(
            url=upload_url_resp.upload_url,
            content=content,
            headers={"Content-Type": mime_type},
            total_size=file_size,
        )

        # 确认上传完成
        self._confirm_upload_completed(
            file_id=upload_url_resp.file.id,
            **metadata
        )

        # 返回文件信息
        return FileUploadResponse(
            file=upload_url_resp.file,
            upload_file=upload_url_resp.upload_file
        )

    def _upload_resumable(
            self,
            file_name: str,
            content: Union[bytes, BinaryIO, Path],
            file_size: int,
            folder_id: Optional[str],
            file_type: str,
            mime_type: str,
            file_hash: str,
            is_temporary: Optional[bool] = False,
            expire_seconds: Optional[int] = None,
            **metadata
    ) -> FileUploadResponse:
        """断点续传实现"""
        # 获取断点续传URL，以及对应的文件和上传文件信息
        upload_url_resp = self._generate_resumable_upload_url(
            file_name=file_name,
            file_size=file_size,
            folder_id=folder_id,
            file_type=file_type,
            mime_type=mime_type,
            file_hash=file_hash,
            is_temporary=is_temporary,
            expire_seconds=expire_seconds if is_temporary and expire_seconds else None,
            **metadata
        )

        # 开启断点续传
        upload_url = self.http_uploader.start_resumable_session(
            url=upload_url_resp.upload_url,
            total_file_size=file_size,
            mine_type=mime_type,
        )

        # 上传文件到对象存储
        self.http_uploader.upload(
            url=upload_url,
            content=content,
            headers={"Content-Type": mime_type},
            total_size=file_size,
            is_resume=True
        )

        # 确认上传完成
        self._confirm_upload_completed(
            file_id=upload_url_resp.file.id,
            **metadata
        )

        # 返回文件信息
        return FileUploadResponse(
            file=upload_url_resp.file,
            upload_file=upload_url_resp.upload_file
        )

    def generate_upload_url(
            self,
            file_name: str,
            file_size: int,
            folder_id: Optional[str] = None,
            file_type: str = "file",
            mime_type: str = None,
            file_hash: str = None,
            is_temporary: Optional[bool] = False,
            expire_seconds: Optional[int] = None,
            **metadata
    ) -> UploadUrlResponse:
        """
        生成上传URL（用于客户端直传）

        Args:
            file_name: 文件名
            file_size: 文件大小
            folder_id: 文件夹ID
            file_type: 文件类型
            mime_type: MIME类型
            file_hash: 文件哈希
            is_temporary: 是否为临时文件
            expire_seconds: 过期秒数
            **metadata: 额外的元数据（如 x-org-id, x-user-id 等）

        Returns:
            上传URL响应
        """
        from ...rpc.gen import file_service_pb2, file_service_pb2_grpc

        stub = self.client.get_stub(file_service_pb2_grpc.FileServiceStub)

        request = file_service_pb2.UploadUrlRequest(
            file_name=file_name,
            file_size=file_size,
            file_type=file_type,
            mime_type=mime_type or "application/octet-stream",
            file_hash=file_hash,
            is_temporary=is_temporary,
            expire_seconds=expire_seconds if is_temporary and expire_seconds else None,
        )

        if folder_id:
            request.folder_id = folder_id

        # 构建元数据
        grpc_metadata = self.client.build_metadata(**metadata)

        response = stub.GenerateUploadUrl(request, metadata=grpc_metadata)

        return UploadUrlResponse(
            file=self._convert_file_info(response.file),
            upload_file=self._convert_upload_file_info(response.upload_file),
            upload_url=response.url
        )

    def upload(
            self,
            file: Union[str, Path, BinaryIO, bytes],
            *,
            folder_id: Optional[str] = None,
            mode: Optional[UploadMode] = UploadMode.NORMAL,
            is_temporary: Optional[bool] = False,
            expire_seconds: Optional[int] = None,
            **metadata
    ) -> FileUploadResponse:
        """
        统一的文件上传接口

        Args:
            file: 文件路径、Path对象、文件对象或字节数据
            folder_id: 目标文件夹ID（可选）
            mode: 上传模式（NORMAL/DIRECT/RESUMABLE/STREAM）
            is_temporary: 是否为临时文件
            expire_seconds: 过期秒数
            **metadata: 额外的元数据

        Returns:
            文件信息
        """
        # 解析文件参数，提取文件信息
        file_name, content, file_size, mime_type, file_type, file_hash = self._extract_file_info(file)

        # 根据文件大小自动选择上传模式
        if mode == UploadMode.NORMAL:
            ten_mb = 1024 * 1024 * 10
            hundred_mb = 1024 * 1024 * 100
            if file_size >= ten_mb and file_size < hundred_mb:  # 10MB
                mode = UploadMode.STREAM  # 大文件自动使用流式上传模式
            elif file_size > hundred_mb:
                mode = UploadMode.RESUMABLE  # 特大文件自动使用断点续传模式

        # 根据上传模式执行不同的上传逻辑
        if mode == UploadMode.NORMAL:
            # 普通上传（通过gRPC）
            return self._upload_file(
                file_name=file_name,
                content=content,
                folder_id=folder_id,
                file_type=file_type,
                mime_type=mime_type,
                is_temporary=is_temporary,
                expire_seconds=expire_seconds if is_temporary and expire_seconds else None,
                **metadata
            )

        elif mode == UploadMode.STREAM:
            # 流式上传
            return self._upload_stream(
                file_name=file_name,
                content=content,
                file_size=file_size,
                folder_id=folder_id,
                file_type=file_type,
                mime_type=mime_type,
                file_hash=file_hash,
                is_temporary=is_temporary,
                expire_seconds=expire_seconds if is_temporary and expire_seconds else None,
                **metadata
            )

        elif mode == UploadMode.RESUMABLE:
            # 断点续传
            return self._upload_resumable(
                file_name=file_name,
                content=content,
                file_size=file_size,
                folder_id=folder_id,
                file_type=file_type,
                mime_type=mime_type,
                file_hash=file_hash,
                is_temporary=is_temporary,
                expire_seconds=expire_seconds if is_temporary and expire_seconds else None,
                **metadata
            )

        else:
            raise ValidationError(f"不支持的上传模式: {mode}")

    def generate_download_url(
            self,
            file_id: str,
            *,
            expire_seconds: Optional[int] = None,
            **metadata
    ) -> str:
        """
        生成下载URL

        Args:
            file_id: 文件ID
            **metadata: 额外的元数据（如 x-org-id, x-user-id 等）

        Returns:
            下载URL
        """
        from ...rpc.gen import file_service_pb2, file_service_pb2_grpc

        stub = self.client.get_stub(file_service_pb2_grpc.FileServiceStub)

        request = file_service_pb2.DownloadUrlRequest(file_id=file_id,
                                                      expire_seconds=expire_seconds if expire_seconds else None)

        # 构建元数据
        grpc_metadata = self.client.build_metadata(**metadata)

        download_url_resp = stub.GenerateDownloadUrl(request, metadata=grpc_metadata)

        return download_url_resp.url

    def download(
            self,
            file_id: str,
            save_path: Optional[Union[str, Path]] = None,
            chunk_size: Optional[int] = None,
            **metadata
    ) -> Union[bytes, Path, Iterator[bytes]]:
        """
        统一的文件下载接口

        Args:
            file_id: 文件ID
            save_path: 保存路径（如果为None，返回字节数据）
            chunk_size: 分片大小
            **metadata: 额外的元数据

        Returns:
            - NORMAL模式：下载的内容（字节）或保存的文件路径
            - STREAM模式：返回迭代器，逐块返回数据
        """

        # 获取下载URL
        download_url = self.generate_download_url(file_id, **metadata)

        return self.http_downloader.download(
            url=download_url,
            save_path=save_path,
            chunk_size=chunk_size,
        )
