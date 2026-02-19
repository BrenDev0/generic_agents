import logging
from src.di import DependencyNotRegistered, Container
from ..application import(
    CreateChat,
    DeleteChat,
    GetChatsCollection,
    GetChatResource
)
from ..dependencies import get_chats_repository
logger = logging.getLogger(__name__)

def get_create_chat_use_case() -> CreateChat:
    try:
        instance_key = "create_chat_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = CreateChat(
            chat_repository=get_chats_repository()
        )

        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")

    return use_case


def get_delete_chat_use_case() -> DeleteChat:
    try:
        instance_key = "delete_chat_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = DeleteChat(
            chat_repository=get_chats_repository()
        )

        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")
        
    return use_case

def get_chat_collection_use_case() -> GetChatsCollection:
    try:
        instance_key = "chat_collection_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = GetChatsCollection(
            chat_repository=get_chats_repository()
        )

        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")
        
    return use_case

def get_chat_resource_use_case() -> GetChatResource:
    try:
        instance_key = "chat_resource_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = GetChatResource(
            chat_repository=get_chats_repository()
        )

        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")
        
    return use_case