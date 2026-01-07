from uuid import UUID
from src.persistence.domain.data_repository import DataRepository
from src.persistence.domain.file_repository import FileRepository
from src.features.knowledge_base.domain.entities import Knowledge
from src.features.knowledge_base.domain.schemas import KnowledgePublic
from src.persistence.domain.exceptions import NotFoundException
from src.security.domain.exceptions import PermissionsException

class DeleteKnowledge:
    def __init__(
        self,
        data_repository: DataRepository,
        file_repository: FileRepository
    ):
        self.__data_repository = data_repository
        self.__file_repository = file_repository

    def execute(
        self,
        knowledge_id: UUID,
        user_id: UUID
    ): 
        knowledge: Knowledge = self.__data_repository.get_one(
            key="knowledge_id",
            value=knowledge_id
        )

        if not knowledge:
            raise NotFoundException("Knowledge resource not found")
        
        if str(knowledge.agent.user_id) != str(user_id):
            raise PermissionsException()
        
        if knowledge.type != "web":
            key = f"{user_id}/knowledge_base/{knowledge.agent_id}/{knowledge.knowledge_id}"

            self.__file_repository.delete(key=key)

        deleted_knoldege: Knowledge = self.__data_repository.delete(
            key="knowledge_id",
            value=knowledge.knowledge_id
        )

        return KnowledgePublic.model_validate(deleted_knoldege, from_attributes=True)

