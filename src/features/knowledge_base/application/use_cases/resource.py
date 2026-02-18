from uuid import UUID
from src.security import PermissionsException
from src.persistence import NotFoundException, DataRepository
from ...domain import Knowledge, KnowledgePublic

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
        knowledge: Knowledge = self.__data_repository.get_one(
            key="knowledge_id",
            value=knowledge_id
        )

        if not knowledge:
            raise NotFoundException()

        if str(knowledge.agent.user_id) != str(user_id):
            raise PermissionsException()
        
        
        return KnowledgePublic.model_validate(knowledge, from_attributes=True)
    
    

