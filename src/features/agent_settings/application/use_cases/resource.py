from uuid import UUID 
from src.persistence import DataRepository, NotFoundException
from ...domain import AgentSettings, AgentSettingsPublic
from src.security import PermissionsException



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
            raise NotFoundException()
        
        if str(setting.agent.user_id) != str(user_id):
            raise PermissionsException()
        
        return AgentSettingsPublic.model_validate(setting, from_attributes=True)
    
    