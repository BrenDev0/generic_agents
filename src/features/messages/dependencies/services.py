import logging
from src.di import Container, DependencyNotRegistered
from src.security import get_encrytpion_service
from ..application import MessageService
logger = logging.getLogger(__name__)

def get_message_service() -> MessageService:
    try:
        instance_key = "message_service"
        service = Container.resolve(instance_key)

    except DependencyNotRegistered:
        service = MessageService(
            encryption=get_encrytpion_service()
        )
        Container.register(instance_key, service)
        logger.debug(f"{instance_key} registered")

    return service

