import logging
from src.di.domain.exceptions import DependencyNotRegistered
from src.di.container import Container
from src.email.application.use_cases.send_email import SendEmail
from src.email.application.use_cases.verification_email import VerificationEmail
logger = logging.getLogger(__name__)


def get_sender_use_case() -> SendEmail:
    try:
        instance_key = "email_sender_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = SendEmail()
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")
    
    return use_case

def get_verification_email_use_case() -> VerificationEmail:
    try:
        instance_key = "verification_email_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = VerificationEmail(
            sender=get_sender_use_case()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")
    
    return use_case

