import logging
from src.di.domain.exceptions import DependencyNotRegistered
from src.di.container import Container
from src.features.agents.application.use_cases import (
    create,
    resource,
    collection,
    update,
    delete
)
from src.features.agents.dependencies.repositories import get_agents_repository
logger = logging.getLogger(__name__)

def get_agent_by_id_use_case() -> resource.GetAgentById:
    try:
        instance_key = "get_agent_by_id_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case  = resource.GetAgentById(
            repository=get_agents_repository()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")
    
    return use_case


def get_agents_by_user_use_case() -> collection.GetAgentsByUser:
    try:
        instance_key = "get_agents_by_user_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case  = collection.GetAgentsByUser(
            repository=get_agents_repository()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")
    
    return use_case


def get_delete_agent_profile_use_case() -> delete.DeleteAgentProfile:
    try:
        instance_key = "delete_agent_profile_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case  = delete.DeleteAgentProfile(
            repository=get_agents_repository()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")
    
    return use_case


def get_create_agent_profile_use_case() -> create.CreateAgentProfile:
    try:
        instance_key = "create_agent_profile_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case  = create.CreateAgentProfile(
            repository=get_agents_repository()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")
    
    return use_case

def get_update_agent_profile_use_case() -> update.UpdateAgentProfile:
    try:
        instance_key = "update_agent_profile_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case  = update.UpdateAgentProfile(
            repository=get_agents_repository()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")
    
    return use_case