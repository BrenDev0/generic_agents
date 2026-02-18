import logging
from src.di import DependencyNotRegistered, Container
from src.security import get_encrytpion_service, get_hashing_service
from ..application import (
    CreateUser,
    GetUser,
    UpdateUser,
    DeleteUser,
    UserLogin
)
from ..dependencies import get_users_repository

logger = logging.getLogger(__name__)

def get_user_use_case() -> GetUser:
    try:
        instance_key = "get_user_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = GetUser(
            repository=get_users_repository(),
            encryption=get_encrytpion_service()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")

    return use_case


def get_create_user_use_case() -> CreateUser:
    try:
        instance_key = "create_user_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = CreateUser(
            repository=get_users_repository(),
            hashing=get_hashing_service(),
            encryption=get_encrytpion_service()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")

    return use_case

def get_login_use_case() -> UserLogin:
    try:
        instance_key = "login_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = UserLogin(
            repository=get_users_repository(),
            hashing=get_hashing_service(),
            encryption=get_encrytpion_service()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")

    return use_case

def get_delete_user_use_case() -> DeleteUser:
    try:
        instance_key = "delete_user_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = DeleteUser(
            repository=get_users_repository(),
            encryption=get_encrytpion_service()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")

    return use_case

def get_update_user_use_case() -> UpdateUser:
    try:
        instance_key = "update_user_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = UpdateUser(
            repository=get_users_repository(),
            encryption=get_encrytpion_service(),
            hashing=get_hashing_service()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")

    return use_case