import logging
from src.di import DependencyNotRegistered, Container
from ..application import Sender
logger = logging.getLogger(__name__)


def get_sender() -> Sender:
    try:
        instance_key = "email_sender"
        service = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        service = Sender()
        Container.register(instance_key, service)
        logger.debug(f"{instance_key} registered")
    
    return service