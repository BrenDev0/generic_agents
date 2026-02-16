from uuid import UUID
from typing import List, Optional
from src.features.knowledge_base.domain import entities, schemas
from src.persistence.domain.data_repository import DataRepository
from src.security.domain.exceptions import PermissionsException
from src.persistence.domain.exceptions import NotFoundException

class GetKnowledgeResource:
    def __init__(
        self,
        data_repository: DataRepository
    ):
        self.__data_repository = data_repository

    def execute(
        self,
        user_id: UUID,
        knowledge_id: UUID
    ): 
        knowledge: entities.Knowledge = self.__data_repository.get_one(
            key="knowledge_id",
            value=knowledge_id
        )

        if not knowledge:
            raise NotFoundException("Knowledge not found")

        if str(knowledge.agent.user_id) != str(user_id):
            raise PermissionsException("Forbidden")
        
        
        return schemas.KnowledgePublic.model_validate(knowledge, from_attributes=True)
    
    

