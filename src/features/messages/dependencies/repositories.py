import logging
from src.di import Container, DependencyNotRegistered
from src.persistence import DataRepository
from ..infrastructure import SqlAlchemyMessageRepository
logger = logging.getLogger(__name__)

def get_message_repository() -> DataRepository:
    try:
        instance_key = "message_repository"
        repository = Container.register(instance_key)
    
    except DependencyNotRegistered:
        repository = SqlAlchemyMessageRepository()
        Container.register(instance_key, repository)
        logger.debug(f"{instance_key} registered")

    
    return repository
