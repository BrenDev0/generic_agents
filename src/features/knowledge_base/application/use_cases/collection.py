from uuid import UUID
from typing import List
from src.features.knowledge_base.domain import entities, schemas
from src.persistence.domain.data_repository import DataRepository
from src.security.domain.exceptions import PermissionsException

class GetKnowledgeCollection:
    def __init__(
        self,
        data_repository: DataRepository
    ):
        self.__data_repository = data_repository

    def execute(
        self,
        user_id: UUID,
        agent_id: UUID
    ): 
        collection: List[entities.Knowledge] = self.__data_repository.get_many(
            key="agent_id",
            value=agent_id
        )

        if not collection:
            return []
        
        if str(collection[0].agent.user_id) != str(user_id):
            raise PermissionsException()
        
        return [
            schemas.KnowledgePublic.model_validate(knowledge, from_attributes=True) for knowledge in collection
        ]
    
    

