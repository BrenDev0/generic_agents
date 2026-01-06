import logging
from src.di.container import Container
from src.di.domain.exceptions import DependencyNotRegistered
from src.features.knowledge_base.application.use_cases.upload import UploadKnowledge
from src.features.knowledge_base.dependencies.repositories import get_knowledge_data_repository, get_knowledge_file_repository
logger = logging.getLogger(__name__)

def get_upload_knowledge_use_case() -> UploadKnowledge:
    try:
        instance_key = "upload_knowledge_use_case",
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = UploadKnowledge(
            data_repository=get_knowledge_data_repository(),
            file_repository=get_knowledge_file_repository()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")
    
    return use_case

