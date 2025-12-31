import logging
from src.di.domain.exceptions import DependencyNotRegistered
from src.di.container import Container
from src.agents.application.use_cases.resource import GetAgentById
from src.agents.application.use_cases.collection import GetAgentsByUser
from src.agents.application.use_cases.create import CreateAgentProfile
from src.agents.application.use_cases.delete import DeleteAgentProfile
from src.agents.application.use_cases.update import UpdateAgentProfile
from src.agents.dependencies.repositories import get_agents_repository
logger = logging.getLogger(__name__)

def get_agent_by_id_use_case() -> GetAgentById:
    try:
        instance_key = "get_agent_by_id_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case  = GetAgentById(
            repository=get_agents_repository()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")
    
    return use_case


def get_agents_by_user_use_case() -> GetAgentsByUser:
    try:
        instance_key = "get_agents_by_user_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case  = GetAgentsByUser(
            repository=get_agents_repository()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")
    
    return use_case


def get_delete_agent_profile_use_case() -> DeleteAgentProfile:
    try:
        instance_key = "delete_agent_profile_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case  = DeleteAgentProfile(
            repository=get_agents_repository()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")
    
    return use_case


def get_create_agent_profile_use_case() -> CreateAgentProfile:
    try:
        instance_key = "create_agent_profile_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case  = CreateAgentProfile(
            repository=get_agents_repository()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")
    
    return use_case

def get_update_agent_profile_use_case() -> UpdateAgentProfile:
    try:
        instance_key = "update_agent_profile_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case  = UpdateAgentProfile(
            repository=get_agents_repository()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")
    
    return use_case