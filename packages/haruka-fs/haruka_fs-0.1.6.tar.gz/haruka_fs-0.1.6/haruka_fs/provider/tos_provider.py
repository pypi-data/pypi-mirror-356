import os
import time
from pathlib import Path
from typing import Optional, Tuple, Dict, Any, Union, Iterator
from loguru import logger

import tos
from tos.exceptions import TosClientError, TosServerError

from haruka_fs.provider.basic_provider import AbstractOssClient, AbstractRangeFile


class TOSRangeDownloader(AbstractRangeFile):
    """TOS 范围下载器，支持按需下载文件片段"""
    
    def __init__(self, client, bucket_name, object_key, size=None, chunk_size=(1024, 20*1024*1024)):
        self.client = client
        self.bucket_name = bucket_name
        self.object_key = object_key
        
        # 如果没有提供size，从TOS获取
        if size is None:
            try:
                response = self.client.head_object(self.bucket_name, self.object_key)
                self.size = response.content_length
            except (TosClientError, TosServerError) as e:
                logger.error(f"获取对象大小失败: {e}")
                raise
        else:
            self.size = size
            
        self.min_chunk_size, self.max_chunk_size = chunk_size
        self.buffer = b""
        self.buffer_start = 0
        self.position = 0

    def read(self, size=-1):
        logger.debug(f"read {size} bytes")
        if size == -1 or self.position + size > self.size:
            size = self.size - self.position

        end_read = self.position + size
        chunks = []
        chunk_size = 0

        while self.position < end_read:
            if self.position < self.buffer_start or self.position >= self.buffer_start + len(self.buffer):
                self._download_chunk(self.position, size - chunk_size)
                
            buffer_offset = self.position - self.buffer_start
            read_size = min(len(self.buffer) - buffer_offset, end_read - self.position)
            chunks.append(self.buffer[buffer_offset:buffer_offset + read_size])
            chunk_size += read_size
            self.position += read_size

        return b''.join(chunks)

    def _download_chunk(self, start_position, chunk_size=None):
        if chunk_size is None:
            chunk_size = self.max_chunk_size
        else:
            chunk_size = min(chunk_size, self.max_chunk_size)
            chunk_size = max(chunk_size, self.min_chunk_size)

        range_start = start_position
        range_end = min(start_position + chunk_size, self.size)  # TOS使用不包含结束位置的范围
        
        logger.debug(f"download chunk {range_start} {range_end}")
        try:
            response = self.client.get_object(
                self.bucket_name, 
                self.object_key, 
                range_start=range_start, 
                range_end=range_end
            )
            self.buffer = response.read()
            self.buffer_start = range_start
        except (TosClientError, TosServerError) as e:
            logger.error(f"下载片段失败: {e}")
            raise

    def seek(self, offset, whence=os.SEEK_SET):
        logger.debug(f"seek {offset} {whence}")
        if whence == os.SEEK_SET:
            self.position = offset
        elif whence == os.SEEK_CUR:
            self.position += offset
        elif whence == os.SEEK_END:
            self.position = self.size + offset
        else:
            raise ValueError("Invalid whence argument")

        if self.position < 0 or self.position > self.size:
            raise ValueError("Seek position is outside the file bounds")

        if self.position < self.buffer_start or self.position >= self.buffer_start + len(self.buffer):
            self.buffer = b""
            self.buffer_start = self.position
        else:
            logger.debug(f"seek in buffer {self.position - self.buffer_start}, remain {len(self.buffer)}")
            self.buffer = self.buffer[self.position - self.buffer_start:]
            self.buffer_start = self.position

    def readline(self):
        """读取一行数据，包含换行符"""
        line = b""
        while True:
            # 如果缓冲区用完或者位置不在缓冲区范围内，重新下载一块
            if self.position < self.buffer_start or self.position >= self.buffer_start + len(self.buffer):
                if self.position >= self.size:
                    break
                self._download_chunk(self.position)

            buffer_offset = self.position - self.buffer_start
            # 在当前缓冲区中查找换行符
            newline_pos = self.buffer.find(b'\n', buffer_offset)
            
            if newline_pos != -1:
                # 找到换行符，读取到换行符为止（包含换行符）
                read_size = newline_pos - buffer_offset + 1
                line += self.buffer[buffer_offset:buffer_offset + read_size]
                self.position += read_size
                break
            else:
                # 没找到换行符，读取当前缓冲区剩余部分
                read_size = len(self.buffer) - buffer_offset
                line += self.buffer[buffer_offset:buffer_offset + read_size]
                self.position += read_size
                
                # 如果已经到文件末尾，退出循环
                if self.position >= self.size:
                    break

        return line

    def readlines(self):
        """读取所有行"""
        lines = []
        while True:
            line = self.readline()
            if not line:
                break
            lines.append(line)
        return lines
    
    def read_range(self, start_offset: int, end_offset: int) -> bytes:
        chunk_size = end_offset - start_offset
        
        if chunk_size <= self.max_chunk_size:
            logger.debug(f"download chunk {start_offset} {end_offset}")
            try:
                response = self.client.get_object(
                    self.bucket_name, 
                    self.object_key, 
                    range_start=start_offset, 
                    range_end=end_offset
                )
                return response.read()
            except (TosClientError, TosServerError) as e:
                logger.error(f"下载范围失败: {e}")
                raise
        else:
            # 分块下载
            chunks = []
            current_offset = start_offset
            while current_offset < end_offset:
                chunk_end = min(current_offset + self.max_chunk_size, end_offset)
                logger.debug(f"download chunk {current_offset} {chunk_end}")
                try:
                    response = self.client.get_object(
                        self.bucket_name,
                        self.object_key,
                        range_start=current_offset,
                        range_end=chunk_end
                    )
                    chunks.append(response.read())
                    current_offset = chunk_end
                except (TosClientError, TosServerError) as e:
                    logger.error(f"下载片段失败: {e}")
                    raise
            return b''.join(chunks)

    def __iter__(self):
        """实现迭代器接口"""
        return self

    def __next__(self):
        """实现迭代器接口"""
        line = self.readline()
        if not line:
            raise StopIteration
        return line

    def tell(self):
        return self.position
    
    def readable(self):
        return True
    
    def seekable(self):
        return True

    def close(self):
        return True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False


class TOSMultipartUploadManager(AbstractRangeFile):
    """TOS 分片上传管理器"""
    
    def __init__(self, client, bucket_name, object_key, chunk_size=(1024, 5*1024*1024)):
        self.client = client
        self.bucket_name = bucket_name
        self.object_key = object_key
        self.min_chunk_size, self.max_chunk_size = chunk_size
        self.upload_id = None
        self.parts = []
        self.buffer = b''
        self.part_number = 1

    def __enter__(self):
        # 初始化分片上传
        try:
            response = self.client.create_multipart_upload(self.bucket_name, self.object_key)
            self.upload_id = response.upload_id
            return self
        except (TosClientError, TosServerError) as e:
            logger.error(f"初始化分片上传失败: {e}")
            raise

    def write(self, data):
        self.buffer += data
        while len(self.buffer) >= self.max_chunk_size:
            self._upload_part()

    def _upload_part(self):
        if len(self.buffer) == 0:
            return
            
        content = self.buffer[:self.max_chunk_size]
        self.buffer = self.buffer[self.max_chunk_size:]
        
        try:
            # TOS 的上传部分
            part = self.client.upload_part(
                self.bucket_name, 
                self.object_key,
                self.upload_id,
                self.part_number,
                content=content
            )
            
            # 保存分片信息
            self.parts.append(part)
            self.part_number += 1
        except (TosClientError, TosServerError) as e:
            logger.error(f"上传分片失败: {e}")
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            # 发生异常时中止上传
            try:
                self.client.abort_multipart_upload(self.bucket_name, self.object_key, self.upload_id)
            except (TosClientError, TosServerError) as e:
                logger.error(f"中止上传失败: {e}")
            return False
            
        # 上传剩余数据
        if self.buffer:
            self._upload_part()
            
        # 完成分片上传
        if self.parts:
            try:
                self.client.complete_multipart_upload(self.bucket_name, self.object_key, self.upload_id, self.parts)
            except (TosClientError, TosServerError) as e:
                logger.error(f"完成上传失败: {e}")
                raise
        return True


class TosClient(AbstractOssClient):
    """TOS客户端封装"""

    def __init__(
        self,
        cred: Tuple[str, str] = None,
        endpoint: str = None,
        region: str = None,
        retry_times: int = 3,
        timeout: int = 60,
    ):
        # 优先使用传入的cred
        if cred:
            self.access_key_id, self.access_key_secret = cred
        else:
            self.access_key_id, self.access_key_secret = self._get_auth()
            
        self.endpoint = endpoint or os.environ.get("TOS_ENDPOINT", "tos-cn-beijing.ivolces.com")
        self.region = region or self._get_region() or os.environ.get("TOS_REGION", "cn-beijing")
        self.retry_times = retry_times
        self.timeout = timeout

        # 创建TOS客户端
        self.client = tos.TosClientV2(
            self.access_key_id, 
            self.access_key_secret, 
            self.endpoint, 
            self.region
        )

    def _get_auth(self) -> Tuple[str, str]:
        """
        获取认证信息，优先从环境变量读取。
        环境变量:
            TOS_ACCESS_KEY_ID
            TOS_ACCESS_KEY_SECRET
        """
        access_key_id = os.environ.get("TOS_ACCESS_KEY_ID")
        access_key_secret = os.environ.get("TOS_ACCESS_KEY_SECRET")
        if access_key_id and access_key_secret:
            return access_key_id, access_key_secret

        logger.info("="*60)
        logger.info("未检测到 TOS_ACCESS_KEY_ID 和 TOS_ACCESS_KEY_SECRET 环境变量！")
        logger.info("请设置环境变量，例如：")
        logger.info("  export TOS_ACCESS_KEY_ID=你的AccessKeyId")
        logger.info("  export TOS_ACCESS_KEY_SECRET=你的AccessKeySecret")
        raise RuntimeError("未检测到TOS鉴权信息，请设置环境变量后重试。")

    def _parse_tos_path(self, tos_path: str) -> Tuple[str, str]:
        """解析TOS路径"""
        if "/" not in tos_path:
            raise ValueError(f"无效的TOS路径: {tos_path}")
        bucket_name, object_key = tos_path.split("/", 1)
        return bucket_name, object_key

    def download_file(
        self,
        tos_path: str,
        local_path: str,
        traffic_limit: Optional[int] = None
    ) -> bool:
        """下载文件"""
        local_path = Path(local_path)
        local_path.parent.mkdir(parents=True, exist_ok=True)

        bucket_name, object_key = self._parse_tos_path(tos_path)

        retry_count = 0
        while retry_count < self.retry_times:
            try:
                # TOS 下载文件
                self.client.get_object_to_file(
                    bucket_name,
                    object_key,
                    str(local_path)
                )
                return True

            except (TosClientError, TosServerError) as e:
                retry_count += 1
                logger.warning(
                    f"下载失败 ({retry_count}/{self.retry_times}): {str(e)}"
                )
                if retry_count >= self.retry_times:
                    logger.error(f"下载失败: {tos_path} -> {local_path}")
                    raise RuntimeError(f"下载文件失败: {str(e)}")
                time.sleep(max(2 ** retry_count, 60))

        return False

    def upload_file(
        self,
        local_path: str,
        tos_path: str,
        traffic_limit: Optional[int] = None
    ) -> bool:
        """上传文件"""
        bucket_name, object_key = self._parse_tos_path(tos_path)

        retry_count = 0
        while retry_count < self.retry_times:
            try:
                # TOS 上传文件
                self.client.put_object_from_file(
                    bucket_name,
                    object_key,
                    str(local_path)
                )
                return True

            except (TosClientError, TosServerError) as e:
                retry_count += 1
                logger.warning(
                    f"上传失败 ({retry_count}/{self.retry_times}): {str(e)}"
                )
                if retry_count >= self.retry_times:
                    logger.error(f"上传失败: {local_path} -> {tos_path}")
                    raise RuntimeError(f"上传文件失败: {str(e)}")
                time.sleep(max(2 ** retry_count, 60))

        return False

    def list_files(
        self,
        prefix: str = "",
        suffix: str = None,
        limit: Optional[int] = None,
    ) -> Iterator[Dict[str, Any]]:
        """列出文件"""
        bucket_name, object_prefix = self._parse_tos_path(prefix)
        idx = 0
        
        try:
            truncated = True
            continuation_token = ''

            while truncated:
                result = self.client.list_objects_type2(
                    bucket_name, 
                    prefix=object_prefix, 
                    continuation_token=continuation_token, 
                    max_keys=1000
                )
                
                for item in result.contents:
                    if suffix and not item.key.lower().endswith(suffix):
                        continue
                    yield {
                        'tos_path': f"{bucket_name}/{item.key}", 
                        'file_size': item.size
                    }
                    idx += 1

                if idx % 10000 == 0:
                    logger.debug(f"已读取 {idx} 个文件，文件太多可能导致处理缓慢")
                
                if limit and idx >= limit:
                    break
                    
                truncated = result.is_truncated
                continuation_token = result.next_continuation_token
                
        except (TosClientError, TosServerError) as e:
            logger.error(f"列出文件失败: {str(e)}")
            raise

        return files

    def file_exists(self, tos_path: str) -> bool:
        """检查文件是否存在"""
        try:
            bucket_name, object_key = self._parse_tos_path(tos_path)
            self.client.head_object(bucket_name, object_key)
            return True
        except (TosClientError, TosServerError) as e:
            if hasattr(e, 'status_code') and e.status_code == 404:
                return False
            logger.error(f"检查文件存在失败: {str(e)}")
            return False

    def get_file_size(self, tos_path: str) -> Optional[int]:
        """获取文件大小"""
        try:
            bucket_name, object_key = self._parse_tos_path(tos_path)
            response = self.client.head_object(bucket_name, object_key)
            return response.content_length
        except (TosClientError, TosServerError) as e:
            logger.error(f"获取文件大小失败: {str(e)}")
            return None

    def open(self, tos_path: str, mode: str = "r", **kwargs) -> Union["TOSRangeDownloader", "TOSMultipartUploadManager"]:
        """
        打开TOS上的文件，支持只读模式('rb')和写入模式('wb')。

        参数:
        tos_path: 文件的TOS路径，格式为 "bucket_name/文件路径"
        mode: 打开模式，仅支持 "rb" (读) 和 "wb" (写)
        kwargs: 可选参数，
            对于读模式，可传入chunk_size，默认值为(1024, 20*1024*1024)（1KB, 20MB）；
            对于写模式，可传入chunk_size，默认值为5*1024*1024（5MB）。

        返回:
        如果mode为"rb"，返回一个TOSRangeDownloader实例，可用于顺序读取TOS文件内容。
        如果mode为"wb"，返回一个TOSMultipartUploadManager实例，建议在with块中使用以确保上传成功。
        """
        if mode not in ("rb", "wb"):
            raise ValueError(f"不支持的模式: {mode}")

        bucket_name, object_key = self._parse_tos_path(tos_path)

        if mode == "rb":
            file_size = self.get_file_size(tos_path)
            if file_size is None:
                raise FileNotFoundError(f"文件不存在: {tos_path}")
            return TOSRangeDownloader(
                self.client,
                bucket_name,
                object_key,
                file_size,
                chunk_size=kwargs.get("chunk_size", (1024, 20 * 1024 * 1024))
            )
        elif mode == "wb":
            return TOSMultipartUploadManager(
                self.client,
                bucket_name,
                object_key,
                chunk_size=kwargs.get("chunk_size", 5 * 1024 * 1024)
            )
        else:
            raise ValueError(f"不支持的模式: {mode}")