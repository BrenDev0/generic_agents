from uuid import UUID
from src.persistence.domain import data_repository, file_repository, exceptions
from src.features.knowledge_base.domain import entities, schemas
from src.features.knowledge_base.utlis.file_size import format_file_size
from src.features.agents.domain.entities import Agent
from src.security.domain.exceptions import PermissionsException
class UploadKnowledge:
    def __init__(
        self,
        data_repository: data_repository.DataRepository,
        file_repository: file_repository.FileRepository,
        agent_repository: data_repository.DataRepository
    ):
        self.__data_repository = data_repository
        self.__file_repository = file_repository
        self.__agent_repository = agent_repository

    def execute(
        self,
        req_data: schemas.CreateKnowledgeRequest,
        user_id: UUID,
        agent_id: UUID,
        filename: str,
        file_type: str,
        file_bytes: bytes
    ): 
        agent: Agent = self.__agent_repository.get_one(
            key="agent_id",
            value=agent_id
        ) 

        if not agent:
            raise exceptions.NotFoundException()
        
        if str(agent.user_id) != str(user_id):
            raise PermissionsException()
        
        file_size = format_file_size(len(file_bytes))

        data = entities.Knowledge(
            **req_data.model_dump(),
            name=filename,
            agent_id=agent.agent_id,
            type=file_type,
            size=file_size
        )

        new_knowledge: entities.Knowledge = self.__data_repository.create(
            data=data
        ) 

        key = f"{user_id}/knowledge_base/{agent_id}/{new_knowledge.knowledge_id}"
        
        try:
            url  = self.__file_repository.upload(
                key=key,
                file_bytes=file_bytes,
                content_type=new_knowledge.type
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
            updated_knowledge: entities.Knowledge = self.__data_repository.update(
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

        return schemas.KnowledgePublic.model_validate(updated_knowledge, from_attributes=True)