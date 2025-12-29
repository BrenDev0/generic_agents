import logging
import strawberry
from typing import List
from uuid import UUID
from src.agents.interface.strawberry.types import AgentType

from src.app.interface.strawberry.middleware.user_auth import UserAuth
from src.agents.dependencies.use_cases import get_agent_by_id_use_case, get_agents_by_user_use_case
from src.shared.domain.exceptions.graphql import GraphQlException
from src.shared.domain.exceptions.permissions import PermissionsException
from src.shared.domain.exceptions.repositories import NotFoundException
logger = logging.getLogger(__name__)

@strawberry.type
class AgentQueries:
    @strawberry.field(
        permission_classes=[UserAuth],
        description="Get agent by id"
    )
    def agent_resource(
        self,
        info: strawberry.Info,
        agent_id: UUID
    ) -> AgentType:
        use_case = get_agent_by_id_use_case()
        user_id = info.context.get("user_id")
        try:
            return use_case.execute(
                user_id=user_id,
                agent_id=agent_id
            )
        
        except (NotFoundException, PermissionsException) as e:
            raise GraphQlException(str(e))
        
        except Exception as e:
            logging.info(str(e))
            raise GraphQlException()
        
    @strawberry.field(
        permission_classes=[UserAuth],
        description="Get all agents for user in auth beaerer"
    )
    def agent_collection(
        self,
        info: strawberry.Info
    ) -> List[AgentType]:
        use_case = get_agents_by_user_use_case()
        user_id = info.context.get("user_id")
        try:
            return use_case.execute(
                user_id=user_id
            )
        
        except Exception as e:
            logger.info(str(e))
            raise GraphQlException()
