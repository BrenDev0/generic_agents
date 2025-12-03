import logging
from src.shared.dependencies.container import Container
from src.shared.domain.exceptions.dependencies import DependencyNotRegistered

from src.security.domain.services.web_token_service import WebTokenService
from src.security.infrastructure.jwt.web_token_service import JwtWebTokenService
logger = logging.getLogger(__name__)

def get_web_token_service() -> WebTokenService:
    try:
        instance_key = "web_token_service"
        service = Container.resolve(instance_key)

    except DependencyNotRegistered:
        service = JwtWebTokenService()
        Container.register(instance_key, service)
        logger.info(f"{instance_key} registered")

    return service