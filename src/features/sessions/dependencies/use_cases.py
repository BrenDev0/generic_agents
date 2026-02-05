import logging
from src.di.container import Container
from src.di.domain.exceptions import DependencyNotRegistered
from src.features.sessions.application.use_cases import update_embeddings_tracker
from src.persistence.dependencies.repositories import get_session_repository

logger = logging.getLogger(__name__)

def get_update_embeddings_tracker_use_case() -> update_embeddings_tracker.UpdateEmbeddingsTracker:
    try:
        instance_key = "update_embeddings_tracker_use_case"
        use_case = Container.resolve(instance_key)

    except DependencyNotRegistered:
        use_case = update_embeddings_tracker.UpdateEmbeddingsTracker(
            session_repository=get_session_repository()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")
    
    return use_case