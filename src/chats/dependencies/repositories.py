import logging
from src.shared.dependencies.container import Container
from src.shared.domain.exceptions.dependencies import DependencyNotRegistered
from src.shared.domain.repositories.data_repository import DataRepository
from src.chats.infrastructure.slqAlchemy.chats_repository import SqlAlchemyChatsRepository
logger = logging.getLogger(__name__)


def get_chats_repository() -> DataRepository:
    try:
        instance_key = "chats_repository"
        repository = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        repository = SqlAlchemyChatsRepository()
        Container.register(instance_key, repository)
        logger.info(f"{instance_key} registered")

    return repository
