from uuid import UUID
from typing import List
from src.persistence.domain import data_repository, file_repository, exceptions
from src.features.knowledge_base.domain import entities, schemas
from src.security.domain.exceptions import PermissionsException

class DeleteAgentKnowledge:
    def __init__(
        self,
        data_repository: data_repository.DataRepository,
        file_repository: file_repository.FileRepository
    ):
        self.__data_repository = data_repository
        self.__file_repository = file_repository

    def execute(
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
        
        keys = [
            f"{user_id}/knowledge_base/{file.agent_id}/{file.knowledge_id}" for file in knowledge
        ]
         
        self.__file_repository.delete(keys=keys)
            

        return 

