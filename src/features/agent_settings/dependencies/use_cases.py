import logging
from src.di.domain.exceptions import DependencyNotRegistered
from src.di.container import Container
from src.features.agent_settings.dependencies import repositories, business_rules
from src.features.agent_settings.application.use_cases import (
    create,
    resource,
    update,
    delete
)
from src.features.agents.dependencies.repositories import get_agents_repository

logger = logging.getLogger(__name__)

def get_agent_settings_create_use_case() -> create.CreateAgentSettings:
    try:
        instance_key = "agent_settings_create_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = create.CreateAgentSettings(
            settings_repository=repositories.get_agent_settings_repository(),
            agents_repository=get_agents_repository(),
            multi_settings_rule=business_rules.get_multi_settings_rule()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")

    return use_case

def get_agent_settings_delete_use_case() -> delete.DeleteAgentSettings:
    try:
        instance_key = "agent_settings_delete_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = delete.DeleteAgentSettings(
            settings_repository=repositories.get_agent_settings_repository()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")

    return use_case

def get_settings_by_id_use_case() -> resource.GetSettingsById:
    try:
        instance_key = "get_setting_by_id_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = resource.GetSettingsById(
            settings_repository=repositories.get_agent_settings_repository()
        )

        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")
    
    return use_case

def get_agent_settings_update_use_case() -> update.UpdateAgentSettings:
    try:
        instance_key = "agent_settings_update_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = update.UpdateAgentSettings(
            settings_repository=repositories.get_agent_settings_repository()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")

    return use_case