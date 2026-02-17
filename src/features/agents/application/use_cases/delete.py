from uuid import UUID
from src.persistence.domain import data_repository, exceptions
from src.features.agents.domain import entities, schemas
from src.security.domain.exceptions import PermissionsException


class DeleteAgentProfile:
    def __init__(
        self,
        repository: data_repository.DataRepository
    ):
        self.__repository = repository

    def execute(
        self,
        user_id: UUID,
        agent_id: UUID
    ): 
        agent: entities.Agent = self.__repository.get_one(
            key="agent_id",
            value=agent_id
        )

        if not agent:
            raise exceptions.NotFoundException()
        
        if str(user_id) != str(agent.user_id):
            raise PermissionsException()
        
        deleted_agent = self.__repository.delete(
            key="agent_id",
            value=agent.agent_id
        )

        return schemas.AgentPublic.model_validate(deleted_agent, from_attributes=True)

