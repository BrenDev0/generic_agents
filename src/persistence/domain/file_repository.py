from abc import ABC, abstractmethod
from typing import List

class FileRepository(ABC):
    @abstractmethod
    def upload(self, key: str, file_bytes: bytes, content_type: str):
        raise NotImplementedError()
    
    def delete(self, keys: List[str]):
        raise NotImplementedError()