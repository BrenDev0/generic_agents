import logging
from src.shared.domain.exceptions.dependencies import DependencyNotRegistered
from src.shared.dependencies.container import Container
from src.agents.application.use_cases.get_agent_by_id import GetAgentById
from src.agents.application.use_cases.get_agents_by_user import GetAgentsByUser
from src.agents.application.use_cases.create_agent_profile import CreateAgentProfile
from src.agents.application.use_cases.delete_agent_profile import DeleteAgentProfile
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
        logger.info(f"{instance_key} registered")
    
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
        logger.info(f"{instance_key} registered")
    
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
        logger.info(f"{instance_key} registered")
    
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
        logger.info(f"{instance_key} registered")
    
    return use_case