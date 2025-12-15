import logging
from src.shared.domain.exceptions.dependencies import DependencyNotRegistered
from src.shared.dependencies.container import Container
from src.users.application.rules.update_password import UpdatePasswordRule
from src.users.dependencies.repositories import get_users_repository
from src.security.dependencies.services import get_hashing_service
logger = logging.getLogger(__name__)

def get_update_password_rule() -> UpdatePasswordRule:
    try:
        instance_key = "update_password_rule"
        business_rule = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        business_rule = UpdatePasswordRule(
            repository=get_users_repository(),
            hashing=get_hashing_service()
        )

        Container.register(instance_key, business_rule)
        logger.info(f"{instance_key} registered")

    return business_rule
