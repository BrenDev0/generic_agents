import logging
from src.di.container import Container
from src.di.domain.exceptions import DependencyNotRegistered
from src.features.knowledge_base.application.use_cases import (
    upload,
    delete,
    update,
    collection,
    delete_by_agent,
    delete_by_user,
    send_to_embed
)
from src.features.knowledge_base.dependencies.repositories import get_knowledge_data_repository, get_knowledge_file_repository
from src.features.agents.dependencies.repositories import get_agents_repository
from src.http.dependencies.clients import get_async_http_client

logger = logging.getLogger(__name__)

def get_upload_knowledge_use_case() -> upload.UploadKnowledge:
    try:
        instance_key = "upload_knowledge_use_case",
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = upload.UploadKnowledge(
            data_repository=get_knowledge_data_repository(),
            file_repository=get_knowledge_file_repository(),
            agent_repository=get_agents_repository()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")
    
    return use_case


def get_delete_knowledge_use_case() -> delete.DeleteKnowledge:
    try:
        instance_key = "delete_knowledge_use_case",
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = delete.DeleteKnowledge(
            data_repository=get_knowledge_data_repository(),
            file_repository=get_knowledge_file_repository()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")
    
    return use_case

def get_delete_knowledge_by_agent_use_case() -> delete_by_agent.DeleteAgentKnowledge:
    try:
        instance_key = "delete_knowledge_by_agent_use_case",
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = delete_by_agent.DeleteAgentKnowledge(
            data_repository=get_knowledge_data_repository(),
            file_repository=get_knowledge_file_repository()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")
    
    return use_case

def get_delete_knowledge_by_user_use_case() -> delete_by_user.DeleteAllKnowledge:
    try:
        instance_key = "delete_knowledge_by_user_use_case",
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = delete_by_user.DeleteAllKnowledge(
            agent_repository=get_agents_repository(),
            file_repository=get_knowledge_file_repository(),
            knowledge_base_repository=get_knowledge_data_repository()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")
    
    return use_case

def get_update_knowledge_use_case() -> update.UpdateKnowledge:
    try:
        instance_key = "update_knowledge_use_case",
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = update.UpdateKnowledge(
            repository=get_knowledge_data_repository()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")
    
    return use_case

def get_knowledge_collection_use_case() -> collection.GetKnowledgeCollection:
    try:
        instance_key = "knowledge_collection_use_case",
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = collection.GetKnowledgeCollection(
            data_repository=get_knowledge_data_repository()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")
    
    return use_case


def get_send_to_embed_use_case() -> send_to_embed.SendToEmbed:
    try:
        instance_key = "send_to_embed_use_case",
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = send_to_embed.SendToEmbed(
            async_http_client=get_async_http_client()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")
    
    return use_case



