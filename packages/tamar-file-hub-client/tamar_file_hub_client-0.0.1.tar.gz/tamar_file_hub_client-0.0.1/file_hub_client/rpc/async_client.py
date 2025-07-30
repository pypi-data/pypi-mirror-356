"""
异步gRPC客户端
"""
from enum import Enum

import grpc
import asyncio
import uuid
import platform
import socket
from typing import Optional, Dict, List, Tuple

from ..enums import Role
from ..errors import ConnectionError
from ..schemas.context import UserContext, RequestContext, FullContext


class AsyncGrpcClient:
    """异步gRPC客户端基类"""

    def __init__(
            self,
            host: str = "localhost",
            port: int = 50051,
            secure: bool = False,
            credentials: Optional[dict] = None,
            options: Optional[list] = None,
            retry_count: int = 3,
            retry_delay: float = 1.0,
            default_metadata: Optional[Dict[str, str]] = None,
            user_context: Optional[UserContext] = None,
            request_context: Optional[RequestContext] = None,
    ):
        """
        初始化异步gRPC客户端
        
        Args:
            host: 服务器地址
            port: 服务器端口
            secure: 是否使用安全连接（TLS）
            credentials: 认证凭据字典（如 {'api_key': 'xxx'}）
            options: gRPC通道选项
            retry_count: 连接重试次数
            retry_delay: 重试延迟（秒）
            default_metadata: 默认的元数据（如 org_id, user_id 等）
            user_context: 用户上下文
            request_context: 请求上下文
        """
        self.host = host
        self.port = port
        self.address = f"{host}:{port}"
        self.secure = secure
        self.credentials = credentials
        self.options = options or []
        self.retry_count = retry_count
        self.retry_delay = retry_delay
        self.default_metadata = default_metadata or {}
        self._channel: Optional[grpc.aio.Channel] = None
        self._stubs = {}
        self._stub_lock = asyncio.Lock()

        # 上下文管理
        self._user_context = user_context
        self._request_context = request_context or self._create_default_request_context()

        # 如果提供了user_context，将其添加到default_metadata
        if self._user_context:
            self.default_metadata.update(self._user_context.to_metadata())

        # 添加请求上下文到default_metadata
        self.default_metadata.update(self._request_context.to_metadata())

    def _create_default_request_context(self) -> RequestContext:
        """创建默认的请求上下文"""
        # 尝试获取客户端IP
        client_ip = None
        try:
            # 获取本机IP（适用于内网环境）
            hostname = socket.gethostname()
            client_ip = socket.gethostbyname(hostname)
        except:
            pass

        # 获取客户端信息
        return RequestContext(
            client_ip=client_ip,
            client_type="python-sdk",
            client_version="1.0.0",  # TODO: 从包版本获取
            user_agent=f"FileHubClient/1.0.0 Python/{platform.python_version()} {platform.system()}/{platform.release()}"
        )

    def _create_channel_credentials(self) -> Optional[grpc.ChannelCredentials]:
        """创建通道凭据"""
        if not self.secure:
            return None

        # 使用默认的SSL凭据
        channel_credentials = grpc.ssl_channel_credentials()

        # 如果有API密钥，创建组合凭据
        if self.credentials and 'api_key' in self.credentials:
            # 创建元数据凭据
            def metadata_callback(context, callback):
                metadata = [('authorization', f"Bearer {self.credentials['api_key']}")]
                callback(metadata, None)

            call_credentials = grpc.metadata_call_credentials(metadata_callback)
            channel_credentials = grpc.composite_channel_credentials(
                channel_credentials,
                call_credentials
            )

        return channel_credentials

    async def connect(self):
        """连接到gRPC服务器（带重试）"""
        if self._channel is not None:
            return

        last_error = None
        for attempt in range(self.retry_count):
            try:
                if attempt > 0:
                    await asyncio.sleep(self.retry_delay)

                channel_credentials = self._create_channel_credentials()

                if channel_credentials:
                    self._channel = grpc.aio.secure_channel(
                        self.address,
                        channel_credentials,
                        options=self.options
                    )
                else:
                    self._channel = grpc.aio.insecure_channel(
                        self.address,
                        options=self.options
                    )

                # 连接
                try:
                    await asyncio.wait_for(self._channel.channel_ready(), timeout=5.0)
                except asyncio.TimeoutError:
                    raise ConnectionError(f"连接超时：{self.address}")

                # 连接成功
                return

            except Exception as e:
                last_error = e
                if attempt < self.retry_count - 1:
                    print(f"连接失败 (尝试 {attempt + 1}/{self.retry_count}): {str(e)}")
                    if self._channel:
                        await self._channel.close()
                        self._channel = None
                else:
                    # 最后一次尝试失败
                    if self._channel:
                        await self._channel.close()
                        self._channel = None

        # 所有重试都失败
        raise ConnectionError(
            f"无法连接到gRPC服务器 {self.address} (尝试了 {self.retry_count} 次): {str(last_error)}"
        )

    async def close(self):
        """关闭连接"""
        if self._channel:
            await self._channel.close()
            self._channel = None
            self._stubs.clear()

    async def get_stub(self, stub_class):
        """
        获取gRPC stub实例
        
        Args:
            stub_class: Stub类
            
        Returns:
            Stub实例
        """
        if not self._channel:
            raise ConnectionError("未连接到gRPC服务器")

        stub_name = stub_class.__name__
        async with self._stub_lock:
            if stub_name not in self._stubs:
                self._stubs[stub_name] = stub_class(self._channel)
            return self._stubs[stub_name]

    def build_metadata(self, **kwargs) -> List[Tuple[str, str]]:
        """
        构建请求元数据
        
        Args:
            **kwargs: 要覆盖或添加的元数据
            
        Returns:
            元数据列表
        """
        metadata = {}

        # 添加默认元数据
        metadata.update(self.default_metadata)

        # 添加/覆盖传入的元数据
        metadata.update(kwargs)

        # 如果没有 request_id，自动生成一个
        if 'x-request-id' not in metadata:
            metadata['x-request-id'] = (
                    self._request_context.extra.get("request_id") or str(uuid.uuid4())
            )

        # 转换为 gRPC 需要的格式
        result = []
        for k, v in metadata.items():
            if v is None:
                continue
            if isinstance(v, Enum):
                v = v.value
            result.append((k, str(v)))

        return result

    def update_default_metadata(self, **kwargs):
        """
        更新默认元数据
        
        Args:
            **kwargs: 要更新的元数据键值对
        """
        self.default_metadata.update(kwargs)

    def set_user_context(self, org_id: str, user_id: str, role: Role = Role.ACCOUNT, actor_id: Optional[str] = None):
        """
        设置用户上下文信息
        
        Args:
            org_id: 组织ID
            user_id: 用户ID
            role: 用户角色（默认为 ACCOUNT）
            actor_id: 操作者ID（如果不同于 user_id）
        """
        self._user_context = UserContext(
            org_id=org_id,
            user_id=user_id,
            role=role,
            actor_id=actor_id
        )
        # 更新到默认元数据
        self.update_default_metadata(**self._user_context.to_metadata())

    def get_user_context(self) -> Optional[UserContext]:
        """获取当前用户上下文"""
        return self._user_context

    def clear_user_context(self):
        """清除用户上下文信息"""
        self._user_context = None
        for key in ['x-org-id', 'x-user-id', 'x-role', 'x-actor-id']:
            self.default_metadata.pop(key, None)

    def set_request_context(self, request_context: RequestContext):
        """设置请求上下文"""
        self._request_context = request_context
        # 更新到默认元数据
        self.update_default_metadata(**self._request_context.to_metadata())

    def get_request_context(self) -> RequestContext:
        """获取当前请求上下文"""
        return self._request_context

    def update_request_context(self, **kwargs):
        """
        更新请求上下文的部分字段
        
        Args:
            **kwargs: 要更新的字段
        """
        if kwargs.get('client_ip'):
            self._request_context.client_ip = kwargs['client_ip']
        if kwargs.get('client_version'):
            self._request_context.client_version = kwargs['client_version']
        if kwargs.get('client_type'):
            self._request_context.client_type = kwargs['client_type']
        if kwargs.get('user_agent'):
            self._request_context.user_agent = kwargs['user_agent']

        # 处理extra字段
        extra = kwargs.get('extra')
        if extra and isinstance(extra, dict):
            self._request_context.extra.update(extra)

        # 更新到默认元数据
        self.update_default_metadata(**self._request_context.to_metadata())

    def get_full_context(self) -> FullContext:
        """获取完整的上下文信息"""
        return FullContext(
            user_context=self._user_context,
            request_context=self._request_context
        )

    async def __aenter__(self) -> "AsyncGrpcClient":
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
