from uuid import UUID
from src.persistence import DataRepository, NotFoundException
from ...domain import AgentSettings, AgentSettingsPublic
from src.security import PermissionsException

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
            raise NotFoundException()

        if str(setting.agent.user_id) != str(user_id):
            raise PermissionsException()
        
        deleted_settings = self.__settings_repository.delete(
            key="setting_id",
            value=setting_id
        )

        return AgentSettingsPublic.model_validate(deleted_settings, from_attributes=True)
