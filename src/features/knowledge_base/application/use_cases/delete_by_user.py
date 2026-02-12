import os
from uuid import UUID
from typing import List
from src.persistence.domain import data_repository, file_repository
from src.features.agents.domain.entities import Agent
from  src.features.knowledge_base.domain.entities import Knowledge
from src.http.domain.async_http_client import AsyncHttpClient
from src.http.utils.hmac_headers import generate_hmac_headers

class DeleteAllKnowledge:
    def __init__(
        self,
        agent_repository: data_repository.DataRepository,
        file_repository: file_repository.FileRepository,
        knowledge_base_repository: data_repository.DataRepository,
        async_http_client: AsyncHttpClient
    ):
        self.__agent_repository = agent_repository
        self.__file_repository = file_repository  
        self.__knowledge_base_repository = knowledge_base_repository 
        self.__async_http_client = async_http_client 

    async def execute(
        self,
        user_id: UUID
    ): 
        agents: List[Agent] = self.__agent_repository.get_many(
            key="user_id",
            value=user_id
        )
        
        if not agents:
            return
        

        ## delete from vector base
        endpoint = f"{os.getenv("LLM_SERVER")}/embeddings/",

        req_body = {
            "key": "user_id",
            "value": user_id
        }

        await self.__async_http_client.request(
            endpoint=endpoint,
            method="DELETE",
            headers=generate_hmac_headers(),
            req_body=req_body
        )
        
        ## delete from bucket 
        keys = []
        for agent in agents:
            knowledge: List[Knowledge] = self.__knowledge_base_repository.get_many(
                key="agent_id",
                value=agent.agent_id
            )

            keys.extend(f"{user_id}/knowledge_base/{file.agent_id}/{file.knowledge_id}" for file in knowledge) 
        
        self.__file_repository.delete(keys=keys)

        ## data in database will delete by cascade
        return 

