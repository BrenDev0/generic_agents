import logging
from src.di.container import Container
from src.di.domain.exceptions import DependencyNotRegistered
from src.features.knowledge_base.application.rules.supported_file_types import IsSupportedFileType
logger = logging.getLogger(__name__)

def get_supported_file_type_rule() -> IsSupportedFileType:
    try:
        instance_key = "supported_file_type_rule",
        rule = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        rule = IsSupportedFileType()
        Container.register(instance_key, rule)
        logger.debug(f"{instance_key} registered")
    
    return rule

