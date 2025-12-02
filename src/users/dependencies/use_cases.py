import logging
from src.shared.domain.exceptions.dependencies import DependencyNotRegistered
from src.shared.dependencies.container import Container
from src.users.application.use_cases.get_user import GetUser
from src.users.dependencies.repositories import get_users_repository
logger = logging.getLogger(__name__)

def get_user_use_case() -> GetUser:
    try:
        instance_key = "get_user_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case =GetUser(
            repository=get_users_repository()
        )
        Container.register(instance_key, use_case)
        logger.info(f"{instance_key} registered")

    return use_case