from uuid import UUID
from src.persistence.domain import data_repository, exceptions
from src.features.agents.domain import entities, schemas
from src.security.domain.exceptions import PermissionsException

class GetAgentById:
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

        if str(agent.user_id) != str(user_id):
            raise PermissionsException()

        
        return schemas.AgentPublic.model_validate(agent, from_attributes=True)

