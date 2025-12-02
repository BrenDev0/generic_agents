import logging
from src.shared.domain.exceptions.dependencies import DependencyNotRegistered
from src.shared.dependencies.container import Container
from src.shared.domain.repositories.data_repository import DataRepository
from src.users.infrastructure.sqlAlchemy.users_repository import SqlAlchemyUsersRepository
logger = logging.getLogger(__name__)

def get_users_repository() -> DataRepository:
    try:
        instance_key = "users_repository"
        repository = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        repository =SqlAlchemyUsersRepository()
        Container.register(instance_key, repository)
        logger.info(f"{instance_key} registered")

    return repository