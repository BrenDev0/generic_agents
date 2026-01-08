import strawberry
import logging
from uuid import UUID
from src.features.knowledge_base.dependencies.use_cases import get_knowledge_collection_use_case
from src.features.knowledge_base.interface.strawberry import types
from src.app.domain.exceptions import GraphQlException
from src.app.interface.strawberry.middleware.user_auth import UserAuth
from src.security.domain.exceptions import PermissionsException
logger = logging.getLogger(__name__)

@strawberry.type
class KnowledgeQueries:
    @strawberry.field(
        permission_classes=[UserAuth],
        description="Get knowledge base by agent id"
    )
    def knowledge_collection(
        self,
        agent_id: UUID,
        info: strawberry.Info
    ) -> types.KnowledgeType:
        user_id = info.context.get("user_id")
        use_case = get_knowledge_collection_use_case()

        try: 
            return use_case.execute(
                user_id=user_id,
                agent_id=agent_id
            )
        
        except PermissionsException as e:
            raise GraphQlException(str(e))
        
        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()
