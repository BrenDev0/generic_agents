from uuid import UUID
from typing import List
from src.persistence.domain import data_repository, file_repository, exceptions
from src.features.knowledge_base.domain import entities, schemas
from src.security.domain.exceptions import PermissionsException
from src.features.agents.domain.entities import Agent
from  src.features.knowledge_base.domain.entities import Knowledge

class DeleteAllKnowledge:
    def __init__(
        self,
        agent_repository: data_repository.DataRepository,
        file_repository: file_repository.FileRepository,
        knowledge_base_repository: data_repository.DataRepository
    ):
        self.__agent_repository = agent_repository
        self.__file_repository = file_repository  
        self.__knowledge_base_repository = knowledge_base_repository  

    def execute(
        self,
        user_id: UUID
    ): 
        agents: List[Agent] = self.__agent_repository.get_many(
            key="user_id",
            value=user_id
        )
        
        if not agents:
            return
        
        keys = []
        for agent in agents:
            knowledge: List[Knowledge] = self.__knowledge_base_repository.get_many(
                key="agent_id",
                value=agent.agent_id
            )

            keys.extend(f"{user_id}/knowledge_base/{file.agent_id}/{file.knowledge_id}" for file in knowledge) 
        
        self.__file_repository.delete(keys=keys)

        return 

