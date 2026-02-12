import os
from uuid import UUID
from typing import List
from src.persistence.domain import data_repository, file_repository, exceptions
from src.features.knowledge_base.domain import entities, schemas
from src.security.domain.exceptions import PermissionsException
from src.http.utils.hmac_headers import generate_hmac_headers
from src.http.domain.async_http_client import AsyncHttpClient

class DeleteAgentKnowledge:
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
        agent_id: UUID,
        user_id: UUID
    ): 
        knowledge: List[entities.Knowledge] = self.__data_repository.get_many(
            key="agent_id",
            value=agent_id
        )

        if not knowledge:
            return
        
        if str(knowledge[0].agent.user_id) != str(user_id):
            raise PermissionsException()
        
        ## delete from vector base
        endpoint = f"{os.getenv("LLM_SERVER")}/embeddings",

        req_body = {
            "key": "agent_id",
            "value": agent_id
        }

        await self.__async_http_client.request(
            endpoint=endpoint,
            method="DELETE",
            headers=generate_hmac_headers(),
            req_body=req_body
        )

        ## delete from bucket 
        keys = [
            f"{user_id}/knowledge_base/{file.agent_id}/{file.knowledge_id}" for file in knowledge
        ]
         
        self.__file_repository.delete(keys=keys)
            
        ## data in data base will delete by cascade
        return 

