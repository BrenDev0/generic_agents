import logging
from src.di import DependencyNotRegistered, Container
from src.persistence import DataRepository
from ..infrastructure import SqlAlchemyUsersRepository
logger = logging.getLogger(__name__)

def get_users_repository() -> DataRepository:
    try:
        instance_key = "users_repository"
        repository = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        repository =SqlAlchemyUsersRepository()
        Container.register(instance_key, repository)
        logger.debug(f"{instance_key} registered")

    return repository