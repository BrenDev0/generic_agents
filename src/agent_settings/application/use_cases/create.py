from uuid import UUID 
from src.shared.domain.repositories.data_repository import DataRepository
from src.agent_settings.domain.schemas import CreateSettingsRequest, AgentSettingsPublic
from src.agents.domain.entities import Agent
from src.agent_settings.domain.entities import AgentSettings
from src.shared.domain.exceptions.repositories import NotFoundException
from src.shared.domain.exceptions.permissions import PermissionsException
from src.agent_settings.application.rules.no_multi_settings import NoMultiSettings

class CreateAgentSettings:
    def __init__(
        self,
        settings_repository: DataRepository,
        agents_repository: DataRepository,
        multi_settings_rule: NoMultiSettings
    ):
        self.__settings_repository = settings_repository
        self.__agents_repository = agents_repository
        self.__multi_settings_rule = multi_settings_rule

    def execute(
        self,
        user_id: UUID,
        agent_id: UUID,
        settings: CreateSettingsRequest
    ):
        self.__multi_settings_rule.validate(
            agent_id=agent_id
        )## Will raise exception if settings found in db

        agent: Agent = self.__agents_repository.get_one( 
            key="agent_id",
            value=agent_id
        ) 

        if not agent: 
            raise NotFoundException("Agent not found")
        
        if str(agent.user_id) != str(user_id):
            raise PermissionsException()
        
        data = AgentSettings(
            agent_id=agent.agent_id,
            **settings.model_dump(by_alias=False)
        )

        new_settings = self.__settings_repository.create(
            data=data
        )

        return AgentSettingsPublic.model_validate(new_settings, from_attributes=True)