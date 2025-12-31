from uuid import UUID
from src.persistence.domain.data_repository import DataRepository
from src.agent_settings.domain.entities import AgentSettings
from src.agent_settings.domain.schemas import AgentSettingsPublic
from src.security.domain.exceptions import PermissionsException
from src.persistence.domain.exceptions import NotFoundException

class DeleteAgentSettings:
    def __init__(
        self,
        settings_repository: DataRepository
    ):
        self.__settings_repository = settings_repository
    
    def execute(
        self,
        user_id: UUID,
        setting_id: UUID
    ): 
        setting: AgentSettings = self.__settings_repository.get_one(
            key="setting_id",
            value=setting_id
        )

        if not setting:
            raise NotFoundException("Settings not found")

        if str(setting.agent.user_id) != str(user_id):
            raise PermissionsException()
        
        deleted_settings = self.__settings_repository.delete(
            key="setting_id",
            value=setting_id
        )

        return AgentSettingsPublic.model_validate(deleted_settings, from_attributes=True)
