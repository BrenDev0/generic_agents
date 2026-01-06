from uuid import UUID
from src.persistence.domain.data_repository import DataRepository
from src.persistence.domain.file_repository import FileRepository
from src.features.knowledge_base.domain.entities import Knowledge
from src.features.knowledge_base.domain.schemas import KnowledgePublic, CreateKnowledgeRequest

class UploadKnowledge:
    def __init__(
        self,
        data_repository: DataRepository,
        file_repository: FileRepository
    ):
        self.__data_repository = data_repository
        self.__file_repository = file_repository

    def execute(
        self,
        req_data: CreateKnowledgeRequest,
        user_id: UUID,
        agent_id: UUID,
        filename: str,
        file_type: str,
        file_bytes: bytes
    ): 
        data = Knowledge(
            **req_data.model_dump(),
            name=filename,
            agent_id=agent_id,
            type=file_type
        )

        new_knowledge: Knowledge = self.__data_repository.create(
            data=data
        ) 

        key = f"{user_id}/knowledge_base/{agent_id}/{new_knowledge.knowledge_id}"
        
        try:
            url  = self.__file_repository.upload(
                key=key,
                file_bytes=file_bytes
            )

        except Exception:
            self.__data_repository.delete(
                key="knowledge_id",
                value=new_knowledge.knowledge_id
            )
            raise

        changes = {
            "url": url
        }

        try:
            updated_knowledge: Knowledge = self.__data_repository.update(
                key="knowledge_id",
                value=new_knowledge.knowledge_id,
                changes=changes
            )
        
        except Exception:
            self.__data_repository.delete(
                key="knowledge_id",
                value=new_knowledge.knowledge_id
            )

            self.__file_repository.delete(
                key=key
            )
            raise

        return KnowledgePublic.model_validate(updated_knowledge, from_attributes=True)