import os
from uuid import UUID
from src.persistence import DataRepository, FileRepository, NotFoundException
from src.security import PermissionsException
from src.http import generate_hmac_headers, AsyncHttpClient
from ...domain import Knowledge, KnowledgePublic

class DeleteKnowledge:
    def __init__(
        self,
        data_repository: DataRepository,
        file_repository: FileRepository,
        async_http_client: AsyncHttpClient
    ):
        self.__data_repository = data_repository
        self.__file_repository = file_repository
        self.__async_http_client = async_http_client

    async def execute(
        self,
        knowledge_id: UUID,
        user_id: UUID
    ): 
        knowledge: Knowledge = self.__data_repository.get_one(
            key="knowledge_id",
            value=knowledge_id
        )

        if not knowledge:
            raise NotFoundException()
        
        if str(knowledge.agent.user_id) != str(user_id):
            raise PermissionsException()
        
        endpoint = f"{os.getenv("LLM_SERVER")}/embeddings/"

        req_body = {
            "key": "knowledge_id",
            "value": str(knowledge_id)
        }

        await self.__async_http_client.request(
            endpoint=endpoint,
            method="DELETE",
            headers=generate_hmac_headers(),
            req_body=req_body
        )
        
        if knowledge.type != "web":
            key = f"{user_id}/knowledge_base/{knowledge.agent_id}/{knowledge.knowledge_id}"

            self.__file_repository.delete(keys=[key])

        deleted_knoldege: Knowledge = self.__data_repository.delete(
            key="knowledge_id",
            value=knowledge.knowledge_id
        )

        return KnowledgePublic.model_validate(deleted_knoldege, from_attributes=True)

