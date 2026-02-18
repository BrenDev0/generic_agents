import logging
from src.di import DependencyNotRegistered, Container
from src.persistence import get_session_repository
from ..application import UpdateEmbeddingsTracker

logger = logging.getLogger(__name__)

def get_update_embeddings_tracker_use_case() -> UpdateEmbeddingsTracker:
    try:
        instance_key = "update_embeddings_tracker_use_case"
        use_case = Container.resolve(instance_key)

    except DependencyNotRegistered:
        use_case = UpdateEmbeddingsTracker(
            session_repository=get_session_repository()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")
    
    return use_case