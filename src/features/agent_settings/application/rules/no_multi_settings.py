from uuid import UUID
from src.persistence import DataRepository
from ...domain import ExistingSettingsException

class NoMultiSettings:
    def __init__(
        self,
        settings_repository: DataRepository
    ):
        self.__repository = settings_repository

    def validate(
        self,
        agent_id: UUID
    ):
        existing_settings = self.__repository.get_one(
            key="agent_id",
            value=agent_id
        )

        if existing_settings:
            raise ExistingSettingsException(f"Agent with id {agent_id} has already been configured. Delete or update existing settings")
        
        return