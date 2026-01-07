from uuid import UUID
from src.persistence.domain.data_repository import DataRepository
from src.persistence.domain.exceptions import NotFoundException
from src.security.domain.exceptions import PermissionsException
from src.features.knowledge_base.domain.entities import Knowledge
from src.features.knowledge_base.domain.schemas import KnowledgePublic, UpdateKnowledgeRequest

class UpdateKnowledge:
    def __init__(
        self,
        repository: DataRepository
    ):
        self.__repository = repository

    
    def execute(
        self,
        user_id: UUID,
        knowledge_id: UUID, 
        changes: UpdateKnowledgeRequest
    ): 
        knowledge: Knowledge = self.__repository.get_one(
            key="knowledge_id",
            value=knowledge_id
        )

        if not knowledge:
            raise NotFoundException("Knowledge resource not found")
        
        if str(knowledge.agent.user_id) != str(user_id):
            raise PermissionsException()
        
        updated_knowledge: Knowledge = self.__repository.update(
            key="knowledge_id",
            value=knowledge.knowledge_id,
            changes=changes.model_dump(exclude_none=True)
        )

        return KnowledgePublic.model_validate(updated_knowledge, from_attributes=True)