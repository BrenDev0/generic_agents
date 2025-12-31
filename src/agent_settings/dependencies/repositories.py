import logging
from src.di.domain.exceptions import DependencyNotRegistered
from src.di.container import Container
from src.persistence.domain.data_repository import DataRepository
from src.agent_settings.infrastructure.sqlAlechemy.agent_settings_repository import SqlAlchemyAgentSettingsRepository
logger = logging.getLogger(__name__)


def get_agent_settings_repository() -> DataRepository:
    try:
        instance_key = "agent_settings_repository"
        repository = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        repository = SqlAlchemyAgentSettingsRepository()
        Container.register(instance_key, repository)
        logger.info(f"{instance_key} registered")

    return repository
