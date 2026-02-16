import httpx
from typing import Dict, Any, Optional
from src.http.domain.async_http_client import AsyncHttpClient


class HttpxAsyncHttpClient(AsyncHttpClient):

    def __init__(self):
        self._client = httpx.AsyncClient(
            timeout=httpx.Timeout(30.0),
            limits=httpx.Limits(
                max_connections=100,
                max_keepalive_connections=20,
            ),
        )

    async def request(
        self,
        endpoint: str,
        method: str,
        req_body: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> httpx.Response:

        response = await self._client.request(
            method=method,
            url=endpoint,
            headers=headers or {},
            json=req_body or {},
        )

        response.raise_for_status()
        return response