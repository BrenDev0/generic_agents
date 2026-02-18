import logging
from src.di import DependencyNotRegistered, Container
from ..application import IsSupportedFileType
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

