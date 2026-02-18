import logging
from src.di import DependencyNotRegistered, Container
from src.features.agents import get_agents_repository
from .repositories import get_agent_settings_repository
from .business_rules import get_multi_settings_rule
from ..application import (
    GetSettingsById,
    CreateAgentSettings,
    DeleteAgentSettings,
    UpdateAgentSettings
)


logger = logging.getLogger(__name__)

def get_agent_settings_create_use_case() -> CreateAgentSettings:
    try:
        instance_key = "agent_settings_create_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = CreateAgentSettings(
            settings_repository=get_agent_settings_repository(),
            agents_repository=get_agents_repository(),
            multi_settings_rule=get_multi_settings_rule()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")

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
        logger.debug(f"{instance_key} registered")

    return use_case

def get_settings_by_id_use_case() -> GetSettingsById:
    try:
        instance_key = "get_setting_by_id_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = GetSettingsById(
            settings_repository=get_agent_settings_repository()
        )

        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")
    
    return use_case

def get_agent_settings_update_use_case() -> UpdateAgentSettings:
    try:
        instance_key = "agent_settings_update_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = UpdateAgentSettings(
            settings_repository=get_agent_settings_repository()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")

    return use_case