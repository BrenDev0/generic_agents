from uuid import UUID
from src.shared.domain.repositories.data_repository import DataRepository
from src.agents.domain.entities import Agent
from src.agents.domain.schemas import AgentPublic
from src.shared.domain.exceptions.repositories import NotFoundException
from src.shared.domain.exceptions.permissions import PermissionsException

class GetAgentById:
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

        if str(agent.user_id) != str(user_id):
            raise PermissionsException()

        
        return AgentPublic.model_validate(agent, from_attributes=True)

