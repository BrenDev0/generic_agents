import logging
from src.di import DependencyNotRegistered, Container
from ..domain import EncryptionService, HashingService, WebTokenService
from ..infrastructure import JwtWebTokenService, BcryptHashingService, FernetEncryptionService
logger = logging.getLogger(__name__)

def get_web_token_service() -> WebTokenService:
    try:
        instance_key = "web_token_service"
        service = Container.resolve(instance_key)

    except DependencyNotRegistered:
        service = JwtWebTokenService()
        Container.register(instance_key, service)
        logger.debug(f"{instance_key} registered")

    return service

def get_hashing_service() -> HashingService:
    try:
        instance_key = "hashing_service"
        service = Container.resolve(instance_key)

    except DependencyNotRegistered:
        service = BcryptHashingService()
        Container.register(instance_key, service)
        logger.debug(f"{instance_key} registered")

    return service

def get_encrytpion_service() -> EncryptionService:
    try:
        instance_key = "encryption_service"
        service = Container.resolve(instance_key)

    except DependencyNotRegistered:
        service = FernetEncryptionService()
        Container.register(instance_key, service)
        logger.debug(f"{instance_key} registered")

    return service