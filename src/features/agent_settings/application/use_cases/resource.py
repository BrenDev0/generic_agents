from uuid import UUID 
from src.persistence.domain import data_repository, exceptions
from src.features.agent_settings.domain import entities, schemas
from src.security.domain.exceptions import PermissionsException



class GetSettingsById:
    def __init__(
        self,
        settings_repository: data_repository.DataRepository
    ):
        self.__repository = settings_repository
    
    def execute(
        self,
        user_id: UUID,
        agent_id: UUID
    ):
        setting: entities.AgentSettings = self.__repository.get_one(
            key="agent_id",
            value=agent_id
        )

        if not setting:
            raise exceptions.NotFoundException("Settings not found")
        
        if str(setting.agent.user_id) != str(user_id):
            raise PermissionsException()
        
        return schemas.AgentSettingsPublic.model_validate(setting, from_attributes=True)
    
    