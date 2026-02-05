from uuid import UUID
from src.persistence.domain import data_repository, exceptions
from src.security.domain.exceptions import PermissionsException
from src.features.knowledge_base.domain import entities, schemas

class UpdateKnowledge:
    def __init__(
        self,
        repository: data_repository.DataRepository
    ):
        self.__repository = repository

    
    def execute(
        self,
        user_id: UUID,
        knowledge_id: UUID, 
        changes: schemas.UpdateKnowledgeRequest
    ): 
        knowledge: entities.Knowledge = self.__repository.get_one(
            key="knowledge_id",
            value=knowledge_id
        )

        if not knowledge:
            raise NotFoundException("Knowledge resource not found")
        
        if str(knowledge.agent.user_id) != str(user_id):
            raise PermissionsException()
        
        updated_knowledge: entities.Knowledge = self.__repository.update(
            key="knowledge_id",
            value=knowledge.knowledge_id,
            changes=changes.model_dump(exclude_none=True)
        )

        return schemas.KnowledgePublic.model_validate(updated_knowledge, by_alias=False)