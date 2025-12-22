import logging
from src.shared.domain.exceptions.dependencies import DependencyNotRegistered
from src.shared.dependencies.container import Container
from src.agent_settings.application.use_cases.create import CreateAgentSetting
from src.agent_settings.application.use_cases.delete import DeleteAgentSetting
from src.agent_settings.application.use_cases.resource import GetSettingById
from src.agents.dependencies.repositories import get_agents_repository
from src.agent_settings.dependencies.repositories import get_agent_settings_repository
logger = logging.getLogger(__name__)

def get_agent_settings_create_use_case() -> CreateAgentSetting:
    try:
        instance_key = "agent_settings_create_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = CreateAgentSetting(
            settings_repository=get_agent_settings_repository(),
            agents_repository=get_agents_repository()
        )
        Container.register(instance_key, use_case)
        logger.info(f"{instance_key} registered")

    return use_case

def get_agent_settings_delete_use_case() -> DeleteAgentSetting:
    try:
        instance_key = "agent_settings_delete_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = DeleteAgentSetting(
            settings_repository=get_agent_settings_repository()
        )
        Container.register(instance_key, use_case)
        logger.info(f"{instance_key} registered")

    return use_case

def get_setting_by_id_use_case():
    try:
        instance_key = "get_setting_by_id_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = GetSettingById(
            repository=get_agent_settings_repository()
        )

        Container.register(instance_key, use_case)
        logger.info(f"{instance_key} registered")
    
    return use_case