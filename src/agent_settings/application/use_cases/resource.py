from uuid import UUID 
from src.shared.domain.repositories.data_repository import DataRepository
from src.agent_settings.domain.entities import AgentSettings
from src.shared.domain.exceptions.permissions import PermissionsException
from src.shared.domain.exceptions.repositories import NotFoundException
from src.agent_settings.domain.schemas import AgentSettingsPublic


class GetSettingsById:
    def __init__(
        self,
        settings_repository: DataRepository
    ):
        self.__repository = settings_repository
    
    def execute(
        self,
        user_id: UUID,
        agent_id: UUID
    ):
        setting: AgentSettings = self.__repository.get_one(
            key="agent_id",
            value=agent_id
        )

        if not setting:
            raise NotFoundException("Settings not found")
        
        if str(setting.agent.user_id) != str(user_id):
            raise PermissionsException()
        
        return AgentSettingsPublic.model_validate(setting, from_attributes=True)
    
    