import logging
from src.shared.domain.exceptions.dependencies import DependencyNotRegistered
from src.shared.dependencies.container import Container
from src.shared.domain.repositories.data_repository import DataRepository
from src.agents.infrastructure.sqlAlchemy.agents_repository import SqlAlchemyAgentsRepository
logger = logging.getLogger(__name__)

def get_agents_repository() -> DataRepository:
    try:
        instance_key = "agents_repository"
        repository = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        repository =SqlAlchemyAgentsRepository()
        Container.register(instance_key, repository)
        logger.info(f"{instance_key} registered")

    return repository