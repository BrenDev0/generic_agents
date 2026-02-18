from uuid import UUID
from src.persistence import DataRepository, NotFoundException
from src.security import PermissionsException
from ...domain import Knowledge, KnowledgePublic, UpdateKnowledgeRequest

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
            raise NotFoundException()
        
        if str(knowledge.agent.user_id) != str(user_id):
            raise PermissionsException()
        
        updated_knowledge: Knowledge = self.__repository.update(
            key="knowledge_id",
            value=knowledge.knowledge_id,
            changes=changes.model_dump(exclude_none=True, by_alias=False)
        )

        return KnowledgePublic.model_validate(updated_knowledge, from_attributes=True)