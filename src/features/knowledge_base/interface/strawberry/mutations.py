import logging
import strawberry
from uuid import UUID
from src.app.interface.strawberry.decorators.req_validation import validate_input_to_model
from src.app.domain.exceptions import GraphQlException
from src.app.interface.strawberry.middleware.user_auth import UserAuth
from src.persistence.domain.exceptions import NotFoundException
from src.security.domain.exceptions import PermissionsException
from src.features.knowledge_base.dependencies import use_cases
from src.features.knowledge_base.interface.strawberry import types, inputs
logger = logging.getLogger(__name__)

@strawberry.type
class KnowledgeBaseMutaions:
    @strawberry.mutation(
        permission_classes=[UserAuth],
        description="Update Knowledge resource"
    )
    @validate_input_to_model
    def update_knowledge(
        self,
        knowledge_id: UUID,
        info: strawberry.Info,
        input: inputs.UpdateKnowledgeInput
    ) -> types.KnowledgeType:
        try:
            user_id = info.context.get("user_id")
            use_case = use_cases.get_update_knowledge_use_case()

        
            return use_case.execute(
                user_id=user_id,
                knowledge_id=knowledge_id,
                changes=input
            )

        except (NotFoundException, PermissionsException) as e:
            raise GraphQlException(str(e))
        
        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()
        
    
    @strawberry.mutation(
        permission_classes=[UserAuth],
        description="Delete knowledge resource"
    )
    def delete_knowledge(
        self,
        knowledge_id: UUID,
        info: strawberry.Info
    ) -> types.KnowledgeType:
        try:
            user_id = info.context.get("user_id")
            use_case = use_cases.get_delete_knowledge_use_case()

        
            return use_case.execute(
                knowledge_id=knowledge_id,
                user_id=user_id
            )
        
        except (NotFoundException, PermissionsException) as e:
            raise GraphQlException(str(e))
        
        except Exception as e: 
            logger.error(str(e))
            raise GraphQlException()