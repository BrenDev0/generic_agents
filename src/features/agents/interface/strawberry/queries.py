import logging
import strawberry
from typing import List
from uuid import UUID
from src.app import GraphQlException
from src.security import PermissionsException, StrawberryUserAuth
from src.persistence import NotFoundException
from ...dependencies import get_agent_by_id_use_case, get_agents_by_user_use_case
from .types import AgentType
logger = logging.getLogger(__name__)

@strawberry.type
class AgentQueries:
    @strawberry.field(
        permission_classes=[StrawberryUserAuth],
        description="Get agent by id"
    )
    def agent_resource(
        self,
        info: strawberry.Info,
        agent_id: UUID
    ) -> AgentType:
        try:
            use_case = get_agent_by_id_use_case()
            user_id = info.context.get("user_id")
            
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
        permission_classes=[StrawberryUserAuth],
        description="Get all agents for user in auth bearer"
    )
    def agent_collection(
        self,
        info: strawberry.Info
    ) -> List[AgentType]:
        try:
            use_case = get_agents_by_user_use_case()
            user_id = info.context.get("user_id")
        
            return use_case.execute(
                user_id=user_id
            )
        
        except Exception as e:
            logger.info(str(e))
            raise GraphQlException()
