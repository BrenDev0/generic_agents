import httpx
import json
from typing import Dict, Any
from src.features.http.domain.async_http_client import AsyncHttpClient

class HttpxAsyncHttpClient(AsyncHttpClient):
    async def post_request(
        self,
        endpoint: str, 
        headers: Dict[str, str],
        req_body: Dict[str, Any]
    ) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url=endpoint,
                headers=headers,
                json=req_body
            )

            return response

    async def get_request(
        self, 
        endpoint: str,
        headers: Dict[str, str],
    ) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url=endpoint,
                headers=headers
            )

            return response