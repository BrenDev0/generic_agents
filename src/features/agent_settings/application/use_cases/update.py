from uuid import UUID
from src.persistence import DataRepository, NotFoundException
from src.security import PermissionsException
from ...domain import AgentSettings, AgentSettingsPublic, UpdateSettingsRequest


class UpdateAgentSettings:
    def __init__(
        self,
        settings_repository: DataRepository
    ):
        self.__repository = settings_repository

    
    def execute(
        self,
        user_id: UUID,
        settings_id: UUID,
        changes: UpdateSettingsRequest
    ):
        setting: AgentSettings = self.__repository.get_one(
            key="setting_id",
            value=settings_id
        )

        if not setting:
            raise NotFoundException()
        
        if str(setting.agent.user_id) != str(user_id):
            raise PermissionsException()
        

        updated_setting = self.__repository.update(
            key="setting_id",
            value=setting.setting_id,
            changes=changes.model_dump(exclude_none=True, by_alias=False)
        )

        return AgentSettingsPublic.model_validate(updated_setting, from_attributes=True)
    


