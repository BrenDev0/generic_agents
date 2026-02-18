import logging
from src.di import Container, DependencyNotRegistered
from ..application import NoMultiSettings
from ..dependencies import get_agent_settings_repository
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
        logger.debug(f"{instance_key} registered")

    return rule