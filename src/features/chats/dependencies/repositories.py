import logging
from src.di.container import Container
from src.di.domain.exceptions import DependencyNotRegistered
from src.persistence import DataRepository
from ..infrastructure import SqlAlchemyChatsRepository
logger = logging.getLogger(__name__)


def get_chats_repository() -> DataRepository:
    try:
        instance_key = "chats_repository"
        repository = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        repository = SqlAlchemyChatsRepository()
        Container.register(instance_key, repository)
        logger.debug(f"{instance_key} registered")

    return repository
