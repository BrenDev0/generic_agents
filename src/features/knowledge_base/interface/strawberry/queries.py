import strawberry
import logging
from uuid import UUID
from typing import List, Optional
from src.app.domain import GraphQlException
from src.security import PermissionsException, StrawberryUserAuth
from ...dependencies import get_knowledge_collection_use_case
from .types import KnowledgeType
logger = logging.getLogger(__name__)

@strawberry.type
class KnowledgeQueries:
    @strawberry.field(
        permission_classes=[StrawberryUserAuth],
        description="Get knowledge base by agent id"
    )
    def knowledge_collection(
        self,
        agent_id: UUID,
        info: strawberry.Info,
        filter: Optional[str] = None
    ) -> List[KnowledgeType]:
        try:
            user_id = info.context.get("user_id")
            use_case = get_knowledge_collection_use_case()

            return use_case.execute(
                user_id=user_id,
                agent_id=agent_id,
                filter=filter
            )
        
        except PermissionsException as e:
            raise GraphQlException(str(e))
        
        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()
