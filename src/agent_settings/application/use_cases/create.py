from uuid import UUID 
from src.shared.domain.repositories.data_repository import DataRepository
from src.agent_settings.domain.schemas import CreateSettingsRequest, AgentSettingsPublic
from src.agents.domain.entities import Agent
from src.agent_settings.domain.entities import AgentSetting
from src.shared.domain.exceptions.repositories import NotFoundException
from src.shared.domain.exceptions.permissions import PermissionsException

class CreateAgentSetting:
    def __init__(
        self,
        settings_repository: DataRepository,
        agents_repository: DataRepository
    ):
        self.__settings_repository = settings_repository
        self.__agents_repository = agents_repository

    def execute(
        self,
        user_id: UUID,
        agent_id: UUID,
        settings: CreateSettingsRequest
    ):
        agent: Agent = self.__agents_repository.get_one(
            key="agent_id",
            value=agent_id
        )

        if not agent: 
            raise NotFoundException("Agent not found")
        
        if str(agent.user_id) != str(user_id):
            raise PermissionsException()
        
        data = AgentSetting(
            agent_id=agent.agent_id,
            **settings.model_dump(by_alias=False)
        )

        new_settings = self.__settings_repository.create(
            data=data
        )

        return AgentSettingsPublic.model_validate(new_settings, from_attributes=True)