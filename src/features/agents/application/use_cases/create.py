from uuid import UUID
from src.persistence.domain.data_repository import DataRepository
from src.features.agents.domain.schemas import CreateAgentProfileRequest
from src.features.agents.domain import entities, schemas


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
        data = entities.Agent(
            user_id=user_id,
            **profile.model_dump()
        )

        new_agent = self.__repository.create(
            data=data
        ) 

        return schemas.AgentPublic.model_validate(new_agent, from_attributes=True)
