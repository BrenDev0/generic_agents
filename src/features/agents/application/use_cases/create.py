from uuid import UUID
from src.persistence.domain.data_repository import DataRepository
from ...domain import CreateAgentProfileRequest, Agent, AgentPublic


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
