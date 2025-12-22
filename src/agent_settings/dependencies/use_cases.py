import logging
from src.shared.domain.exceptions.dependencies import DependencyNotRegistered
from src.shared.dependencies.container import Container
from src.agent_settings.application.use_cases.create import CreateAgentSettings
from src.agent_settings.application.use_cases.delete import DeleteAgentSettings
from src.agent_settings.application.use_cases.resource import GetSettingsById
from src.agents.dependencies.repositories import get_agents_repository
from src.agent_settings.dependencies.repositories import get_agent_settings_repository
logger = logging.getLogger(__name__)

def get_agent_settings_create_use_case() -> CreateAgentSettings:
    try:
        instance_key = "agent_settings_create_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = CreateAgentSettings(
            settings_repository=get_agent_settings_repository(),
            agents_repository=get_agents_repository()
        )
        Container.register(instance_key, use_case)
        logger.info(f"{instance_key} registered")

    return use_case

def get_agent_settings_delete_use_case() -> DeleteAgentSettings:
    try:
        instance_key = "agent_settings_delete_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = DeleteAgentSettings(
            settings_repository=get_agent_settings_repository()
        )
        Container.register(instance_key, use_case)
        logger.info(f"{instance_key} registered")

    return use_case

def get_setting_by_id_use_case() -> GetSettingsById:
    try:
        instance_key = "get_setting_by_id_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = GetSettingsById(
            repository=get_agent_settings_repository()
        )

        Container.register(instance_key, use_case)
        logger.info(f"{instance_key} registered")
    
    return use_case