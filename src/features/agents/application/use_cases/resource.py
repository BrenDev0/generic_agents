from uuid import UUID
from src.persistence import DataRepository, NotFoundException
from src.security import PermissionsException
from ...domain import Agent, AgentPublic

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
            raise NotFoundException()

        if str(agent.user_id) != str(user_id):
            raise PermissionsException()

        
        return AgentPublic.model_validate(agent, from_attributes=True)

