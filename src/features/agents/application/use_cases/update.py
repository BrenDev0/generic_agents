import logging
from uuid import UUID
from src.persistence.domain.data_repository import DataRepository
from src.features.agents.domain.entities import Agent
from src.security.domain.exceptions import PermissionsException
from src.persistence.domain.exceptions import NotFoundException
from src.features.agents.domain.schemas import AgentPublic, UpdatAgentProfileRequest
logger = logging.getLogger(__name__)

class UpdateAgentProfile:
    def __init__(
        self,
        repository: DataRepository
    ):
        self.__repository = repository

    def execute(
        self,
        user_id: UUID,
        agent_id: UUID,
        changes: UpdatAgentProfileRequest
    ):
        agent: Agent = self.__repository.get_one(
            key="agent_id",
            value=agent_id
        )

        if not agent:
            raise NotFoundException("Agent not found")
        
        if str(agent.user_id) != str(user_id):
            raise PermissionsException()
        
        updated_agent: Agent = self.__repository.update(
            key="agent_id",
            value=agent_id,
            changes=changes.model_dump(exclude_none=True)
        )

        return AgentPublic.model_validate(updated_agent, from_attributes=True)



