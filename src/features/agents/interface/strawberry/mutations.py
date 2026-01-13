import logging
import strawberry
from uuid import UUID
from src.features.agents.interface.strawberry import types, inputs
from src.features.agents.dependencies.use_cases import (
    get_create_agent_profile_use_case, 
    get_delete_agent_profile_use_case,
    get_update_agent_profile_use_case
)
from src.app.interface.strawberry.middleware.user_auth import UserAuth
from src.app.domain.exceptions import GraphQlException
from src.app.interface.strawberry.decorators.req_validation import validate_input_to_model
from src.security.domain.exceptions import PermissionsException
from src.persistence.domain.exceptions import NotFoundException
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
        input: inputs.CreateAgentProfileInput
    ) -> types.AgentType: 
        try:
            use_case = get_create_agent_profile_use_case()
            user_id = info.context.get("user_id")

            return use_case.execute(
                user_id=user_id,
                profile=input.to_pydantic()
            )

        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()
        
    
    @strawberry.mutation(
        description="Delete agent profile",
        permission_classes=[UserAuth]
    )
    def agent_delete(
        self,
        info: strawberry.Info,
        agent_id: UUID
    ) -> types.AgentType: 
        try:
            use_case = get_delete_agent_profile_use_case()
            user_id = info.context.get("user_id")

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
        input: inputs.UpdateAgentProfileInput,
        agent_id: UUID
    ) -> types.AgentType:
        try:
            use_case = get_update_agent_profile_use_case()
            user_id = info.context.get("user_id")

            return use_case.execute(
                user_id=user_id,
                agent_id=agent_id,
                changes=input.to_pydantic()
            )
        
        except (NotFoundException, PermissionsException) as e:
            raise GraphQlException(str(e))
        
        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()