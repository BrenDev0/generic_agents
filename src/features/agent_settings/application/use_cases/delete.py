from uuid import UUID
from src.persistence.domain import data_repository, exceptions
from src.features.agent_settings.domain import entities, schemas
from src.security.domain.exceptions import PermissionsException

class DeleteAgentSettings:
    def __init__(
        self,
        settings_repository: data_repository.DataRepository
    ):
        self.__settings_repository = settings_repository
    
    def execute(
        self,
        user_id: UUID,
        setting_id: UUID
    ): 
        setting: entities.AgentSettings = self.__settings_repository.get_one(
            key="setting_id",
            value=setting_id
        )

        if not setting:
            raise exceptions.NotFoundException("Settings not found")

        if str(setting.agent.user_id) != str(user_id):
            raise PermissionsException()
        
        deleted_settings = self.__settings_repository.delete(
            key="setting_id",
            value=setting_id
        )

        return schemas.AgentSettingsPublic.model_validate(deleted_settings, from_attributes=True)
