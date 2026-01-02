import logging
from src.di.container import Container
from src.di.domain.exceptions import DependencyNotRegistered
from src.features.chats.application.use_cases.chat_create import CreateChat
from src.features.chats.dependencies.repositories import get_chats_repository
logger = logging.getLogger(__name__)

def get_creat_chat_use_case() -> CreateChat:
    try:
        instance_key = "create_chat_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = CreateChat(
            repository=get_chats_repository()
        )

        Container.register(instance_key, use_case)
        logger.debg(f"{instance_key} registered")
    return use_case