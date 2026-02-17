import os
from uuid import UUID
from src.persistence.domain import data_repository, file_repository, exceptions
from src.features.knowledge_base.domain import entities, schemas
from src.security.domain.exceptions import PermissionsException
from src.http.domain.async_http_client import AsyncHttpClient
from src.http.utils.hmac_headers import generate_hmac_headers

class DeleteKnowledge:
    def __init__(
        self,
        data_repository: data_repository.DataRepository,
        file_repository: file_repository.FileRepository,
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
        knowledge: entities.Knowledge = self.__data_repository.get_one(
            key="knowledge_id",
            value=knowledge_id
        )

        if not knowledge:
            raise exceptions.NotFoundException()
        
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

        deleted_knoldege: entities.Knowledge = self.__data_repository.delete(
            key="knowledge_id",
            value=knowledge.knowledge_id
        )

        return schemas.KnowledgePublic.model_validate(deleted_knoldege, from_attributes=True)

