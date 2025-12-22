from uuid import UUID 
from src.shared.domain.repositories.data_repository import DataRepository
from src.agent_settings.domain.entities import AgentSetting
from src.shared.domain.exceptions.permissions import PermissionsException
from src.shared.domain.exceptions.repositories import NotFoundException
from src.agent_settings.domain.schemas import AgentSettingsPublic


class GetSettingById:
    def __init__(
        self,
        repository: DataRepository
    ):
        self.__repository = repository

    
    def execute(
        self,
        user_id: UUID,
        setting_id: UUID
    ):
        setting: AgentSetting = self.__repository.get_one(
            key="setting_id",
            value=setting_id
        )

        if not setting:
            raise NotFoundException("Settings not found")
        
        if str(setting.agent.user_id) != str(user_id):
            raise PermissionsException()
        
        return AgentSettingsPublic.model_validate(setting, from_attributes=True)
    
    