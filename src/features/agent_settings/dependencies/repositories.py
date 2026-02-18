import logging
from src.di import Container, DependencyNotRegistered
from src.persistence import DataRepository
from ..infrastructure import SqlAlchemyAgentSettingsRepository
logger = logging.getLogger(__name__)


def get_agent_settings_repository() -> DataRepository:
    try:
        instance_key = "agent_settings_repository"
        repository = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        repository = SqlAlchemyAgentSettingsRepository()
        Container.register(instance_key, repository)
        logger.debug(f"{instance_key} registered")

    return repository
