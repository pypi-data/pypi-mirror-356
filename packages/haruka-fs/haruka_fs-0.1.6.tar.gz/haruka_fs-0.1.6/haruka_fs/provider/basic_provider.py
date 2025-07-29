from abc import ABC, abstractmethod
from typing import Tuple, Optional, Dict, Any, Union, Iterator

class AbstractOssClient(ABC):
    """OSS客户端抽象基类"""

    @abstractmethod
    def __init__(
        self,
        cred: Tuple[str, str] = None,
        retry_times: int = 3,
        timeout: int = 60,
    ):
        pass

    @abstractmethod
    def download_file(
        self,
        oss_path: str,
        local_path: str,
        traffic_limit: Optional[int] = None
    ) -> bool:
        """下载文件"""
        pass

    @abstractmethod
    def upload_file(
        self,
        local_path: str,
        oss_path: str,
        traffic_limit: Optional[int] = None
    ) -> bool:
        """上传文件"""
        pass

    @abstractmethod
    def list_files(
        self,
        prefix: str = "",
        suffix: str = None,
        limit: Optional[int] = None,
    ) -> Iterator[Dict[str, Any]]:
        """列出文件"""
        pass

    @abstractmethod
    def file_exists(self, oss_path: str) -> bool:
        """检查文件是否存在"""
        pass

    @abstractmethod
    def get_file_size(self, oss_path: str) -> Optional[int]:
        """获取文件大小"""
        pass

    @abstractmethod
    def open(self, oss_path: str, mode: str = "r", **kwargs) -> Union[Any, Any]:
        pass

class AbstractRangeFile(ABC):
    @abstractmethod
    def read(self, size=-1):
        pass

    @abstractmethod
    def seek(self, offset, whence=0):
        pass

    @abstractmethod
    def tell(self):
        pass

    @abstractmethod
    def close(self):
        pass

    def readline(self):
        raise NotImplementedError

    def readlines(self):
        raise NotImplementedError
    
    def read_range(self, start_offset: int, end_offset: int):
        raise NotImplementedError

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    def readable(self):
        return True

    def seekable(self):
        return True