import logging
from src.di import DependencyNotRegistered, Container
from src.persistence import DataRepository
from ..infrastructure import SqlAlchemyAgentsRepository
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