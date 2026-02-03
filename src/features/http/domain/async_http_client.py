from abc import ABC, abstractmethod
from typing import Dict, Any

class AsyncHttpClient(ABC):

    @abstractmethod
    async def post_request(
        self,
        endpoint: str,
        headers: Dict[str, str],
        req_body: Dict[str, Any]
    ):
        raise NotImplementedError
    
    @abstractmethod
    async def get_request(
        self,
        endpoint: str,
        headers: Dict[str, str],
    ): 
        raise NotImplementedError

