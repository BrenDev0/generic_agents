from uuid import UUID
from src.shared.domain.repositories.data_repository import DataRepository
from src.agents.domain.schemas import CreateAgentProfileRequest
from src.agents.domain.entities import Agent
from src.agents.domain.schemas import AgentPublic


class CreateAgentProfile:
    def __init__(
        self,
        repository: DataRepository
    ):
        self.__repository = repository

    def execute(
        self,
        user_id: UUID,
        profile: CreateAgentProfileRequest
    ):
        data = Agent(
            user_id=user_id,
            **profile.model_dump()
        )

        new_agent = self.__repository.create(
            data=data
        ) 

        return AgentPublic.model_validate(new_agent, from_attributes=True)
