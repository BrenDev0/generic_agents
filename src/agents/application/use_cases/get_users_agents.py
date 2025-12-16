from uuid import UUID
from src.shared.domain.repositories.data_repository import DataRepository
from src.agents.domain.schemas import AgentPublic

class GetUsersAgents:
    def __init__(
        self,
        repository: DataRepository
    ):
        self.__repository = repository

    
    def execute(
        self,
        user_id: UUID
    ): 
        agents = self.__repository.get_many(
            key="user_id",
            value=user_id
        )

        return [
            AgentPublic.model_validate(agent, from_attributes=True) for agent in agents
        ] if agents else []
    
        