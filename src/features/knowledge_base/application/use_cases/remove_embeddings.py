import os
from uuid import UUID
from src.http import generate_hmac_headers, AsyncHttpClient

class RemoveEmbeddings:
    def __init__(
        self,
        async_http_client: AsyncHttpClient
    ):
        self.__async_http_client = async_http_client

    async def execute(
        self,
        knowledge_id: UUID
    ):
        endpoint = f"{os.getenv("LLM_SERVER")}/embeddings/"
        
        body = {
            "key": "knowledge_id",
            "value": str(knowledge_id)
        }

        await self.__async_http_client.request(
            endpoint=endpoint,
            method="DELETE",
            headers=generate_hmac_headers(),
            req_body=body
        )
