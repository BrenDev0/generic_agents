import logging
from src.di import DependencyNotRegistered, Container
from ..application import (
    VerificationEmail
)
from .services import get_sender
logger = logging.getLogger(__name__)


def get_verification_email_use_case() -> VerificationEmail:
    try:
        instance_key = "verification_email_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = VerificationEmail(
            sender=get_sender()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")
    
    return use_case

