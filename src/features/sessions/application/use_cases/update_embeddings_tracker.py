import json
from uuid import UUID
from typing import Dict, Union
from src.persistence.domain.session_repository import SessionRepository

class UpdateEmbeddingsTracker:
    def __init__(
        self,
        session_repository: SessionRepository
    ):
        self.__session_repository = session_repository

    def execute(
        self,
        agent_id: UUID,
        knowledge_id: UUID,
        update: Dict[str, Union[str,int]]
    ):
        key = f"{agent_id}_embeddings_tracker"

        session = self.__session_repository.get_session(key=key)

        if session:
            session[str(knowledge_id)] = update
        
        else:
            session = {
                str(knowledge_id): update
            }

        self.__session_repository.set_session(
            key=key,
            value=json.dumps(session)
        )