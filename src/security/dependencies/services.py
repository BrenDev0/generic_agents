import logging
from src.di.container import Container
from src.di.domain.exceptions import DependencyNotRegistered

from src.security.domain.services import (
    hashing,
    encryption,
    web_token
)
from src.security.infrastructure.jwt.web_token_service import JwtWebTokenService
from src.security.infrastructure.bcrypt.hashing_service import BcryptHashingService
from src.security.infrastructure.fernet.encryption_service import FernetEncryptionService
logger = logging.getLogger(__name__)

def get_web_token_service() -> web_token.WebTokenService:
    try:
        instance_key = "web_token_service"
        service = Container.resolve(instance_key)

    except DependencyNotRegistered:
        service = JwtWebTokenService()
        Container.register(instance_key, service)
        logger.debug(f"{instance_key} registered")

    return service

def get_hashing_service() -> hashing.HashingService:
    try:
        instance_key = "hashing_service"
        service = Container.resolve(instance_key)

    except DependencyNotRegistered:
        service = BcryptHashingService()
        Container.register(instance_key, service)
        logger.debug(f"{instance_key} registered")

    return service

def get_encrytpion_service() -> encryption.EncryptionService:
    try:
        instance_key = "encryption_service"
        service = Container.resolve(instance_key)

    except DependencyNotRegistered:
        service = FernetEncryptionService()
        Container.register(instance_key, service)
        logger.debug(f"{instance_key} registered")

    return service