from uuid import UUID
from src.shared.domain.repositories.data_repository import DataRepository
from src.agent_settings.domain.entities import AgentSettings
from src.agent_settings.domain.schemas import AgentSettingsPublic, UpdateSettingsRequest
from src.shared.domain.exceptions.permissions import PermissionsException
from src.shared.domain.exceptions.repositories import NotFoundException

class UpdateAgentSettings:
    def __init__(
        self,
        repository: DataRepository
    ):
        self.__repository = repository

    
    def execute(
        self,
        user_id: UUID,
        setting_id: UUID,
        changes: UpdateSettingsRequest
    ):
        setting: AgentSettings = self.__repository.get_one(
            key="setting_id",
            value=setting_id
        )

        if not setting:
            raise NotFoundException("Settings not found")
        
        if str(setting.agent.user_id) != str(user_id):
            raise PermissionsException()
        

        updated_setting = self.__repository.update(
            key="setting_id",
            value=setting.setting_id,
            changes=changes.model_dump(exclude_none=True)
        )

        return AgentSettingsPublic.model_validate(updated_setting, from_attributes=True)
    


