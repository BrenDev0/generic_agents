from uuid import UUID
from typing import List, Optional
from src.persistence import DataRepository
from src.security import PermissionsException
from ...domain import Knowledge, KnowledgePublic

class GetKnowledgeCollection:
    def __init__(
        self,
        data_repository: DataRepository
    ):
        self.__data_repository = data_repository

    def execute(
        self,
        user_id: UUID,
        agent_id: UUID,
        filter: Optional[str] = None
    ): 
        collection: List[Knowledge] = self.__data_repository.get_many(
            key="agent_id",
            value=agent_id
        )

        if not collection:
            return []
        
        if str(collection[0].agent.user_id) != str(user_id):
            raise PermissionsException()
        
        return [
            KnowledgePublic.model_validate(knowledge, from_attributes=True) for knowledge in collection
        ] if not filter else [
            KnowledgePublic.model_validate(knowledge, from_attributes=True) for knowledge in collection if knowledge.state and knowledge.state.lower() == filter.lower()
        ]
    
    

