import logging
from src.di import DependencyNotRegistered, Container
from src.http.dependencies.clients import get_async_http_client
from ..application import (
    GetKnowledgeCollection,
    UpdateKnowledge,
    UploadKnowledge,
    DeleteAgentKnowledge,
    DeleteAllKnowledge,
    DeleteKnowledge,
    RemoveEmbeddings,
    SendToEmbed,
    GetKnowledgeResource
)
from ..dependencies import get_knowledge_data_repository, get_knowledge_file_repository

logger = logging.getLogger(__name__)

def get_upload_knowledge_use_case() -> UploadKnowledge:
    try:
        instance_key = "upload_knowledge_use_case",
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        from src.features.agents import get_agents_repository
        use_case = UploadKnowledge(
            data_repository=get_knowledge_data_repository(),
            file_repository=get_knowledge_file_repository(),
            agent_repository=get_agents_repository()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")
    
    return use_case


def get_delete_knowledge_use_case() -> DeleteKnowledge:
    try:
        instance_key = "delete_knowledge_use_case",
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = DeleteKnowledge(
            data_repository=get_knowledge_data_repository(),
            file_repository=get_knowledge_file_repository(),
            async_http_client=get_async_http_client()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")
    
    return use_case

def get_delete_knowledge_by_agent_use_case() -> DeleteAgentKnowledge:
    try:
        instance_key = "delete_knowledge_by_agent_use_case",
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = DeleteAgentKnowledge(
            data_repository=get_knowledge_data_repository(),
            file_repository=get_knowledge_file_repository(),
            async_http_client=get_async_http_client()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")
    
    return use_case

def get_delete_knowledge_by_user_use_case() -> DeleteAllKnowledge:
    try:
        instance_key = "delete_knowledge_by_user_use_case",
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = DeleteAllKnowledge(
            agent_repository=get_agents_repository(),
            file_repository=get_knowledge_file_repository(),
            knowledge_base_repository=get_knowledge_data_repository(),
            async_http_client=get_async_http_client()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")
    
    return use_case

def get_update_knowledge_use_case() -> UpdateKnowledge:
    try:
        instance_key = "update_knowledge_use_case",
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = UpdateKnowledge(
            repository=get_knowledge_data_repository()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")
    
    return use_case

def get_knowledge_collection_use_case() -> GetKnowledgeCollection:
    try:
        instance_key = "knowledge_collection_use_case",
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = GetKnowledgeCollection(
            data_repository=get_knowledge_data_repository()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")
    
    return use_case


def get_send_to_embed_use_case() -> SendToEmbed:
    try:
        instance_key = "send_to_embed_use_case",
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = SendToEmbed(
            async_http_client=get_async_http_client()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")
    
    return use_case

def get_delete_embeddings_use_case() -> RemoveEmbeddings:
    try:
        instance_key = "delete_embeddings_use_case",
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = RemoveEmbeddings(
            async_http_client=get_async_http_client()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")
    
    return use_case

def get_knowledge_resource_use_case() -> GetKnowledgeResource:
    try:
        instance_key = "knowledge_resource_use_case",
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = GetKnowledgeResource(
            data_repository=get_knowledge_data_repository()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")
    
    return use_case





