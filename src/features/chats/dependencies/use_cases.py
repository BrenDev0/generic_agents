import logging
from src.di.container import Container
from src.di.domain.exceptions import DependencyNotRegistered
from src.features.chats.application.use_cases import(
    create
)
from src.features.chats.dependencies.repositories import get_chats_repository
logger = logging.getLogger(__name__)

def get_creat_chat_use_case() -> create.CreateChat:
    try:
        instance_key = "create_chat_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = create.CreateChat(
            repository=get_chats_repository()
        )

        Container.register(instance_key, use_case)
        logger.debg(f"{instance_key} registered")
    return use_case