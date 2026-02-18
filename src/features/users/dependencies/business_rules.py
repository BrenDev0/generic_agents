import logging
from src.di import DependencyNotRegistered, Container
from src.security import get_hashing_service
from ..application import(
    UniqueEmailRule,
    UpdatePasswordRule,
    UserExists
)
from ..dependencies import get_users_repository
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
        logger.debug(f"{instance_key} registered")

    return business_rule

def get_unique_email_rule() -> UniqueEmailRule:
    try:
        instance_key = "unique_email_rule"
        business_rule = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        business_rule = UniqueEmailRule(
            repository=get_users_repository(),
            hashing=get_hashing_service()
        )

        Container.register(instance_key, business_rule)
        logger.debug(f"{instance_key} registered")

    return business_rule


def get_user_exists_rule() -> UserExists:
    try:
        instance_key = "user_exists_rule"
        business_rule = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        business_rule = UserExists(
            repository=get_users_repository(),
            hashing=get_hashing_service()
        )

        Container.register(instance_key, business_rule)
        logger.debug(f"{instance_key} registered")

    return business_rule

