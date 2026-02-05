import logging
from src.di.container import Container
from src.di.domain.exceptions import DependencyNotRegistered
from src.persistence.domain import session_repository
from src.persistence.infrastructure.redis.session_repository import RedisSessionRepository

logger = logging.getLogger(__name__)

def get_session_repository() -> session_repository.SessionRepository:
    try:
        instance_key = "session_repository"
        repository = Container.resolve(instance_key)

    except DependencyNotRegistered:
        repository = RedisSessionRepository()
        Container.register(instance_key, repository)
        logger.debug(f"{instance_key} registered")

    return repository