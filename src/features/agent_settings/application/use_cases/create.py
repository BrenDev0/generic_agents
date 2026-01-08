from uuid import UUID 
from src.persistence.domain import data_repository, exceptions
from src.security.domain.exceptions import PermissionsException
from src.features.agent_settings.domain import schemas, entities
from src.features.agent_settings.application.rules.no_multi_settings import NoMultiSettings
from src.features.agents.domain.entities import Agent

class CreateAgentSettings:
    def __init__(
        self,
        settings_repository: data_repository.DataRepository,
        agents_repository: data_repository.DataRepository,
        multi_settings_rule: NoMultiSettings
    ):
        self.__settings_repository = settings_repository
        self.__agents_repository = agents_repository
        self.__multi_settings_rule = multi_settings_rule

    def execute(
        self,
        user_id: UUID,
        agent_id: UUID,
        settings: schemas.CreateSettingsRequest
    ):
        self.__multi_settings_rule.validate(
            agent_id=agent_id
        )## Will raise exception if settings found in db

        agent: Agent = self.__agents_repository.get_one( 
            key="agent_id",
            value=agent_id
        ) 

        if not agent: 
            raise exceptions.NotFoundException("Agent not found")
        
        if str(agent.user_id) != str(user_id):
            raise PermissionsException()
        
        data = entities.AgentSettings(
            agent_id=agent.agent_id,
            **settings.model_dump(by_alias=False)
        )

        new_settings = self.__settings_repository.create(
            data=data
        )

        return schemas.AgentSettingsPublic.model_validate(new_settings, from_attributes=True)