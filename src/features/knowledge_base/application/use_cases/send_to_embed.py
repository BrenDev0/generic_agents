import os
import json
from uuid import UUID
from src.http.domain.async_http_client import AsyncHttpClient
from src.http.utils.hmac_headers import generate_hmac_headers

class SendToEmbed:
    def __init__(
        self,
        async_http_client: AsyncHttpClient
    ):
        self.__async_http_client = async_http_client

    async def execute(
        self,
        user_id: UUID,
        agent_id: UUID,
        knowledge_id: UUID,
        connection_id: UUID,
        file_type: str,
        file_url: str
    ):
        endpoint = f"{os.getenv("LLM_SERVER")}/documents/knowledge-base"
        
        body = {
            "user_id": str(user_id),
            "agent_id": str(agent_id),
            "knowledge_id": str(knowledge_id),
            "connection_id": str(connection_id),
            "file_type": file_type,
            "file_url": file_url
        }

        await self.__async_http_client.request(
            endpoint=endpoint,
            method="POST",
            headers=generate_hmac_headers(),
            req_body=body
        )
