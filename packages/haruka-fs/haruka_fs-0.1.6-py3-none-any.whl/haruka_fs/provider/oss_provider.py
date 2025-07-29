import haruka_fs.utils.load_env

import time
from pathlib import Path
from typing import Optional, Tuple, List, Dict, Any, Iterator, Union
from loguru import logger

import os
import oss2
from oss2.models import OSS_TRAFFIC_LIMIT

from haruka_fs.provider.basic_provider import AbstractOssClient, AbstractRangeFile

class OSSRangeDownloader(AbstractRangeFile):
    def __init__(self, bucket, key, size=None, chunk_size=(1024, 20*1024*1024)):
        self.bucket = bucket
        self.key = key
        # 如果没有提供size,从bucket获取
        if size is None:
            header = self.bucket.head_object(self.key)
            self.size = header.content_length
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
        range_end = min(start_position + chunk_size - 1, self.size - 1)  # OSS2需要包含结束位置
        
        # OSS2的范围下载格式是包含结束位置的
        logger.debug(f"download chunk {range_start} {range_end}")
        response = self.bucket.get_object(
            self.key, 
            byte_range=(range_start, range_end)
        )
        self.buffer = response.read()
        self.buffer_start = range_start

    def seek(self, offset, whence=os.SEEK_SET):
        logger.debug(f"seek {offset} {whence}")
        if whence == os.SEEK_SET:
            self.position = offset
        elif whence == os.SEEK_CUR:
            self.position += offset
        elif whence == os.SEEK_END:
            self.position = self.size + offset
        else:
            raise ValueError(f"Invalid whence argument {whence}, only support {os.SEEK_SET}, {os.SEEK_CUR}, {os.SEEK_END}")

        if self.position < 0 or self.position > self.size:
            raise ValueError(f"Seek position {self.position} is outside the file bounds {self.size}")

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
        chunk_size = end_offset - start_offset + 1
        
        if chunk_size <= self.max_chunk_size:
            logger.debug(f"download chunk {start_offset} {end_offset}")
            response = self.bucket.get_object(
                self.key, 
                byte_range=(start_offset, end_offset)
            )
            return response.read()
        else:
            # 分块下载
            chunks = []
            current_offset = start_offset
            while current_offset <= end_offset:
                chunk_end = min(current_offset + self.max_chunk_size - 1, end_offset)
                logger.debug(f"download chunk {current_offset} {chunk_end}")
                response = self.bucket.get_object(
                    self.key,
                    byte_range=(current_offset, chunk_end)
                )
                chunks.append(response.read())
                current_offset = chunk_end + 1
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


class OSSMultipartUploadManager(AbstractRangeFile):
    def __init__(self, bucket, key, chunk_size=(1024, 5*1024*1024)):
        self.bucket = bucket
        self.key = key
        self.min_chunk_size, self.max_chunk_size = chunk_size
        self.upload_id = None
        self.parts = []
        self.buffer = b''
        self.part_number = 1

    def __enter__(self):
        # 初始化分片上传
        self.upload_id = self.bucket.init_multipart_upload(self.key).upload_id
        return self

    def write(self, data):
        self.buffer += data
        while len(self.buffer) >= self.max_chunk_size:
            self._upload_part()

    def _upload_part(self):
        if len(self.buffer) == 0:
            return
            
        content = self.buffer[:self.max_chunk_size]
        self.buffer = self.buffer[self.max_chunk_size:]
        
        # OSS2的上传部分返回ETag
        result = self.bucket.upload_part(
            self.key, 
            self.upload_id,
            self.part_number,
            content
        )
        
        # 保存分片信息
        self.parts.append(oss2.models.PartInfo(
            self.part_number, 
            result.etag
        ))
        self.part_number += 1

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            # 发生异常时中止上传
            self.bucket.abort_multipart_upload(self.key, self.upload_id)
            return False
            
        # 上传剩余数据
        if self.buffer:
            self._upload_part()
            
        # 完成分片上传
        if self.parts:
            self.bucket.complete_multipart_upload(self.key, self.upload_id, self.parts)
        return True


class OssClient(AbstractOssClient):
    """OSS客户端封装"""

    def __init__(
        self,
        cred: Tuple[str, str] = None,
        endpoint: str = None,
        retry_times: int = 3,
        timeout: int = 60,
    ):
        # 优先使用传入的cred
        if cred:
            self.access_key_id, self.access_key_secret = cred
        else:
            self.access_key_id, self.access_key_secret = self._get_auth()
        self.endpoint = endpoint or os.environ.get("OSS_ENDPOINT", "oss-cn-beijing-internal.aliyuncs.com")
        self.retry_times = retry_times
        self.timeout = timeout

        # 创建认证对象
        self.auth = oss2.Auth(self.access_key_id, self.access_key_secret)
        # 创建Bucket对象
        self.buckets = {}

    def _get_auth(self) -> Tuple[str, str]:
        """
        获取认证信息，优先从环境变量读取。
        环境变量:
            OSS_ACCESS_KEY_ID
            OSS_ACCESS_KEY_SECRET
        如果没有，提示用户设置环境变量，并给出STS授权说明。
        """
        access_key_id = os.environ.get("OSS_ACCESS_KEY_ID")
        access_key_secret = os.environ.get("OSS_ACCESS_KEY_SECRET")
        if access_key_id and access_key_secret:
            return access_key_id, access_key_secret

        logger.info("="*60)
        logger.info("未检测到 OSS_ACCESS_KEY_ID 和 OSS_ACCESS_KEY_SECRET 环境变量！")
        logger.info("请设置环境变量，例如：")
        logger.info("  export OSS_ACCESS_KEY_ID=你的AccessKeyId")
        logger.info("  export OSS_ACCESS_KEY_SECRET=你的AccessKeySecret")
        raise RuntimeError("未检测到OSS鉴权信息，请设置环境变量后重试。")

    def get_bucket(self, oss_path: str) -> Tuple[oss2.Bucket, str]:
        """获取Bucket对象"""
        bucket_name, bucket_path = oss_path.split("/", 1)
        endpoint = self.endpoint
        if bucket_name not in self.buckets:
            self.buckets[bucket_name] = oss2.Bucket(self.auth, endpoint, bucket_name)
        return self.buckets[bucket_name], bucket_path

    def download_file(
        self,
        oss_path: str,
        local_path: str,
        traffic_limit: Optional[int] = None
    ) -> bool:
        """下载文件"""
        local_path = Path(local_path)
        local_path.parent.mkdir(parents=True, exist_ok=True)

        bucket, bucket_path = self.get_bucket(oss_path)

        retry_count = 0
        while retry_count < self.retry_times:
            try:
                headers = {}
                if traffic_limit:
                    headers[OSS_TRAFFIC_LIMIT] = str(traffic_limit)

                bucket.get_object_to_file(
                    bucket_path,
                    str(local_path),
                    headers=headers,
                    progress_callback=lambda uploaded, total: logger.debug(
                        f"下载进度: {uploaded}/{total} ({uploaded/total*100:.2f}%)"
                    )
                )
                return True

            except Exception as e:
                retry_count += 1
                logger.warning(
                    f"下载失败 ({retry_count}/{self.retry_times}): {str(e)}"
                )
                if retry_count >= self.retry_times:
                    logger.error(f"下载失败: {oss_path} -> {local_path}")
                    raise RuntimeError(f"下载文件失败: {str(e)}")
                time.sleep(max(2 ** retry_count, 60))

        return False

    def upload_file(
        self,
        local_path: str,
        oss_path: str,
        traffic_limit: Optional[int] = None
    ) -> bool:
        """上传文件"""
        bucket, bucket_path = self.get_bucket(oss_path)

        retry_count = 0
        while retry_count < self.retry_times:
            try:
                headers = {}
                if traffic_limit:
                    headers[OSS_TRAFFIC_LIMIT] = str(traffic_limit)

                bucket.put_object_from_file(
                    bucket_path,
                    str(local_path),
                    headers=headers,
                    progress_callback=lambda uploaded, total: logger.debug(
                        f"上传进度: {uploaded}/{total} ({uploaded/total*100:.2f}%)"
                    )
                )
                return True

            except Exception as e:
                retry_count += 1
                logger.warning(
                    f"上传失败 ({retry_count}/{self.retry_times}): {str(e)}"
                )
                if retry_count >= self.retry_times:
                    logger.error(f"上传失败: {local_path} -> {oss_path}")
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
        idx = 0
        bucket, bucket_prefix = self.get_bucket(prefix)
        for obj in oss2.ObjectIterator(bucket, prefix=bucket_prefix, max_keys=1000):
            if not obj.is_prefix():  # 不是目录
                if suffix and not obj.key.endswith(suffix):
                    continue
                yield {'oss_path': f"{bucket.bucket_name}/{obj.key}", 'file_size': obj.size}
                idx += 1

            if idx % 10000 == 0:
                logger.debug(f"已读取 {idx} 个文件，文件太多可能导致处理缓慢")
            
            if limit and idx >= limit:
                break

    def file_exists(self, oss_path: str) -> bool:
        """检查文件是否存在"""
        try:
            bucket, bucket_path = self.get_bucket(oss_path)
            return bucket.object_exists(bucket_path)
        except Exception as e:
            logger.error(f"检查文件存在失败: {str(e)}")
            return False

    def get_file_size(self, oss_path: str) -> Optional[int]:
        """获取文件大小"""
        try:
            bucket, bucket_path = self.get_bucket(oss_path)
            header = bucket.head_object(bucket_path)
            return header.content_length
        except Exception as e:
            logger.error(f"获取文件大小失败: {str(e)}")
            return None

    def open(self, oss_path: str, mode: str = "r", **kwargs) -> Union["OSSRangeDownloader", "OSSMultipartUploadManager"]:
        """
        打开OSS上的文件，支持只读模式('r')和写入模式('w')。

        参数:
        oss_path: 文件的OSS路径，格式为 "bucket_name/文件路径"
        mode: 打开模式，仅支持 "rb" (读) 和 "wb" (写)
        kwargs: 可选参数，
            对于读模式，可传入chunk_size，默认值为(1024, 20*1024*1024)（1KB, 20MB）；
            对于写模式，可传入chunk_size，默认值为(1024, 5*1024*1024)（1KB, 5MB）。

        返回:
        如果mode为"rb"，返回一个OSSRangeDownloader实例，可用于顺序读取OSS文件内容。
        如果mode为"wb"，返回一个OSSMultipartUploadManager实例，建议在with块中使用以确保上传成功。
        """
        if mode not in ("rb", "wb"):
            raise ValueError(f"不支持的模式: {mode}")
        
        chunk_size = kwargs.get("chunk_size", (1024, 20 * 1024 * 1024))
        if isinstance(chunk_size, int):
            chunk_size = (chunk_size, chunk_size)

        bucket, bucket_key = self.get_bucket(oss_path)

        if mode == "rb":
            file_size = self.get_file_size(oss_path)
            if file_size is None:
                raise FileNotFoundError(f"文件不存在: {oss_path}")
            return OSSRangeDownloader(
                bucket,
                bucket_key,
                file_size,
                chunk_size=chunk_size
            )
        elif mode == "wb":
            return OSSMultipartUploadManager(
                bucket,
                bucket_key,
                chunk_size=chunk_size
            )
        else:
            raise ValueError(f"不支持的模式: {mode}")
