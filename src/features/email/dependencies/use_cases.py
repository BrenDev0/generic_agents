import logging
from src.di.domain.exceptions import DependencyNotRegistered
from src.di.container import Container
from src.features.email.application.use_cases import (
    send_email,
    verification_email
)
logger = logging.getLogger(__name__)


def get_sender_use_case() -> send_email.SendEmail:
    try:
        instance_key = "email_sender_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = send_email.SendEmail()
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")
    
    return use_case

def get_verification_email_use_case() -> verification_email.VerificationEmail:
    try:
        instance_key = "verification_email_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = verification_email.VerificationEmail(
            sender=get_sender_use_case()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")
    
    return use_case

