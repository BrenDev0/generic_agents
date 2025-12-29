import logging
from src.shared.domain.exceptions.dependencies import DependencyNotRegistered
from src.shared.dependencies.container import Container
from src.agent_settings.application.rules.no_multi_settings import NoMultiSettings
from src.agent_settings.dependencies.repositories import get_agent_settings_repository
logger = logging.getLogger(__name__)


def get_multi_settings_rule() -> NoMultiSettings:
    try:
        instance_key = "multi_settings_rule"
        rule = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        rule = NoMultiSettings(
            settings_repository=get_agent_settings_repository()
        )
        Container.register(instance_key, rule)
        logger.info(f"{instance_key} registered")

    return rule