import os
from uuid import UUID
from src.features.http.domain.async_http_client import AsyncHttpClient
from src.features.http.utils.hmac_headers import generate_hmac_headers

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
        file_type: str,
        file_url: str
    ):
        endpoint = f"{os.getenv("LLM_SERVER")}/documents/knowlege-base/{agent_id}"
        
        body = {
            "user_id": str(user_id),
            "knowledge_id": str(knowledge_id),
            "file_type": file_type,
            "file_url": file_url
        }

        return await self.__async_http_client.post_request(
            endpoint=endpoint,
            headers=generate_hmac_headers(),
            req_body=body
        )

