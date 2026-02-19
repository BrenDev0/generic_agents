import logging
from src.di import Container, DependencyNotRegistered
from ..application import CreateMessage, GetMessageCollection
from .services import get_message_service
from .repositories import get_message_repository
logger = logging.getLogger(__name__)

def get_create_message_use_case() -> CreateMessage:
    try:
        instance_key = "create_message_use_case"
        use_case = Container.resolve(instance_key)

    except DependencyNotRegistered:
        use_case = CreateMessage(
            message_repository=get_message_repository(),
            message_service=get_message_service()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")

    return use_case


def get_messages_collection_use_case() -> GetMessageCollection:
    try:
        instance_key = "message_collection_use_case"
        use_case = Container.resolve(instance_key)

    except DependencyNotRegistered:
        use_case = GetMessageCollection(
            message_repository=get_message_repository(),
            message_service=get_message_service()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")

    return use_case

