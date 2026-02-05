import os
import json
from uuid import UUID
from src.http.domain.async_http_client import AsyncHttpClient
from src.http.utils.hmac_headers import generate_hmac_headers
from src.persistence.domain.session_repository import SessionRepository

class SendToEmbed:
    def __init__(
        self,
        async_http_client: AsyncHttpClient,
        session_repository: SessionRepository
    ):
        self.__async_http_client = async_http_client
        self.__session_repository = session_repository

    async def execute(
        self,
        user_id: UUID,
        agent_id: UUID,
        knowledge_id: UUID,
        file_type: str,
        file_url: str
    ):
        endpoint = f"{os.getenv("LLM_SERVER")}/documents/knowledge-base"
        
        body = {
            "user_id": str(user_id),
            "agent_id": str(agent_id),
            "knowledge_id": str(knowledge_id),
            "connection_id": str(user_id),
            "file_type": file_type,
            "file_url": file_url
        }

        await self.__async_http_client.request(
            endpoint=endpoint,
            method="POST",
            headers=generate_hmac_headers(),
            req_body=body
        )



        embedding_tracker = {
            str(knowledge_id): {
                "stage": "Enviando documento...",
                "status": "Enviado",
                "progress": 100
            }
        }
        session_key = f"{agent_id}_embeddings_tracker"

        self.__session_repository.set_session(
            key=session_key,
            value=json.dumps(embedding_tracker)
        )

