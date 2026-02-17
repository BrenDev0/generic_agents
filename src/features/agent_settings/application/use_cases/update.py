from uuid import UUID
from src.persistence.domain import data_repository, exceptions
from src.features.agent_settings.domain import entities, schemas
from src.security.domain.exceptions import PermissionsException

class UpdateAgentSettings:
    def __init__(
        self,
        settings_repository: data_repository.DataRepository
    ):
        self.__repository = settings_repository

    
    def execute(
        self,
        user_id: UUID,
        settings_id: UUID,
        changes: schemas.UpdateSettingsRequest
    ):
        setting: entities.AgentSettings = self.__repository.get_one(
            key="setting_id",
            value=settings_id
        )

        if not setting:
            raise exceptions.NotFoundException()
        
        if str(setting.agent.user_id) != str(user_id):
            raise PermissionsException()
        

        updated_setting = self.__repository.update(
            key="setting_id",
            value=setting.setting_id,
            changes=changes.model_dump(exclude_none=True, by_alias=False)
        )

        return schemas.AgentSettingsPublic.model_validate(updated_setting, from_attributes=True)
    


