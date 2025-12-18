import logging
import strawberry
from uuid import UUID
from src.app.interface.strawberry.middleware.user_auth import UserAuth
from src.agents.interface.strawberry.inputs import (
    CreateAgentProfileInput,
    UpdateAgentProfileInput
)
from src.agents.interface.strawberry.types import AgentType
from src.agents.dependencies.use_cases import (
    get_create_agent_profile_use_case, 
    get_delete_agent_profile_use_case,
    get_update_agent_profile_use_case
)
from src.shared.domain.exceptions.graphql import GraphQlException
from src.shared.domain.exceptions.permissions import PermissionsException
from src.shared.domain.exceptions.repositories import NotFoundException
logger = logging.getLogger(__name__)

@strawberry.type
class AgentMutations:
    @strawberry.mutation(
        permission_classes=[UserAuth],
        description="Create agent profile"
    )
    def agent_create(
        self,
        info: strawberry.Info,
        input: CreateAgentProfileInput
    ) -> AgentType: 
        use_case = get_create_agent_profile_use_case()
        user_id = info.context.get("user_id")

        try:
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
    ) -> AgentType: 
        use_case = get_delete_agent_profile_use_case()
        user_id = info.context.get("user_id")

        try:
            return use_case.execute(
                user_id=user_id,
                agent_id=agent_id
            )
        
        except NotFoundException as e:
            raise GraphQlException(str(e))
        
        except PermissionsException as e:
            raise GraphQlException(str(e))

        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()
        
    
    @strawberry.mutation(
        permission_classes=[UserAuth],
        description="Update agent profile"
    )
    def update_agent(
        self,
        info: strawberry.Info,
        input: UpdateAgentProfileInput,
        agent_id: UUID
    ):
        use_case = get_update_agent_profile_use_case()
        user_id = info.context.get("user_id")

        try:
            return use_case.execute(
                user_id=user_id,
                agent_id=agent_id,
                changes=input.to_pydantic()
            )
        
        except NotFoundException as e:
            raise GraphQlException(str(e))
        
        except PermissionError as e:
            raise GraphQlException(str(e))
        
        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()