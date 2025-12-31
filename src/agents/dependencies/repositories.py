import logging
from src.di.domain.exceptions import DependencyNotRegistered
from src.di.container import Container
from src.persistence.domain.data_repository import DataRepository
from src.agents.infrastructure.sqlAlchemy.agents_repository import SqlAlchemyAgentsRepository
logger = logging.getLogger(__name__)

def get_agents_repository() -> DataRepository:
    try:
        instance_key = "agents_repository"
        repository = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        repository =SqlAlchemyAgentsRepository()
        Container.register(instance_key, repository)
        logger.debug(f"{instance_key} registered")

    return repository