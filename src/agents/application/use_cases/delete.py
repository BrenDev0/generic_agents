from uuid import UUID
from src.shared.domain.repositories.data_repository import DataRepository
from src.agents.domain.entities import Agent
from src.shared.domain.exceptions.repositories import NotFoundException
from src.shared.domain.exceptions.permissions import PermissionsException
from src.agents.domain.schemas import AgentPublic

class DeleteAgentProfile:
    def __init__(
        self,
        repository: DataRepository
    ):
        self.__repository = repository

    def execute(
        self,
        user_id: UUID,
        agent_id: UUID
    ): 
        agent: Agent = self.__repository.get_one(
            key="agent_id",
            value=agent_id
        )

        if not agent:
            raise NotFoundException("Agent not found")
        
        if str(user_id) != str(agent.user_id):
            raise PermissionsException()
        
        deleted_agent = self.__repository.delete(
            key="agent_id",
            value=agent.agent_id
        )

        return AgentPublic.model_validate(deleted_agent, from_attributes=True)

