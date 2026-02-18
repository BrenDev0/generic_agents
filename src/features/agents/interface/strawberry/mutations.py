import logging
import strawberry
from uuid import UUID
from src.app import GraphQlException
from src.app.interface.strawberry.middleware.user_auth import UserAuth
from src.app.interface.strawberry.decorators.req_validation import validate_input_to_model
from src.security import PermissionsException
from src.persistence import NotFoundException
from src.features.knowledge_base.dependencies.use_cases import get_delete_knowledge_by_agent_use_case
from .inputs import CreateAgentProfileInput, UpdateAgentProfileInput
from .types import AgentType
from ...dependencies import (
    get_create_agent_profile_use_case, 
    get_delete_agent_profile_use_case,
    get_update_agent_profile_use_case
)

logger = logging.getLogger(__name__)

@strawberry.type
class AgentMutations:
    @strawberry.mutation(
        permission_classes=[UserAuth],
        description="Create agent profile"
    )
    @validate_input_to_model
    def agent_create(
        self,
        info: strawberry.Info,
        input: CreateAgentProfileInput
    ) -> AgentType: 
        try:
            use_case = get_create_agent_profile_use_case()
            user_id = info.context.get("user_id")

            return use_case.execute(
                user_id=user_id,
                profile=input
            )

        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()
        
    
    @strawberry.mutation(
        description="Delete agent profile",
        permission_classes=[UserAuth]
    )
    async def agent_delete(
        self,
        info: strawberry.Info,
        agent_id: UUID
    ) -> AgentType: 
        try:
            use_case = get_delete_agent_profile_use_case()
            user_id = info.context.get("user_id")
            delete_uploads_use_case = get_delete_knowledge_by_agent_use_case()

            await delete_uploads_use_case.execute(
                agent_id=agent_id,
                user_id=user_id
            )
            return use_case.execute(
                user_id=user_id,
                agent_id=agent_id
            )
        
        except (NotFoundException, PermissionsException) as e:
            raise GraphQlException(str(e))

        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()
        
    
    @strawberry.mutation(
        permission_classes=[UserAuth],
        description="Update agent profile"
    )
    @validate_input_to_model
    def update_agent(
        self,
        info: strawberry.Info,
        input: UpdateAgentProfileInput,
        agent_id: UUID
    ) -> AgentType:
        try:
            use_case = get_update_agent_profile_use_case()
            user_id = info.context.get("user_id")

            return use_case.execute(
                user_id=user_id,
                agent_id=agent_id,
                changes=input
            )
        
        except (NotFoundException, PermissionsException) as e:
            raise GraphQlException(str(e))
        
        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()