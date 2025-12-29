import strawberry
import logging
from uuid import UUID
from src.agent_settings.dependencies.use_cases import get_settings_by_id_use_case
from src.shared.domain.exceptions.graphql import GraphQlException 
from src.shared.domain.exceptions.permissions import PermissionsException
from src.shared.domain.exceptions.repositories import NotFoundException
from src.app.interface.strawberry.middleware.user_auth import UserAuth
from src.agent_settings.interface.strawberry.types import AgentSettingsType
logger = logging.getLogger(__name__)

@strawberry.type
class AgentSettingsQueries:
    @strawberry.field(
        description="Get agents Settings by agent id",
        permission_classes=[UserAuth]
    )
    def agent_settings_resource(
        self,
        agent_id: UUID,
        info: strawberry.Info
    ) -> AgentSettingsType:
        user_id = info.context.get("user_id")
        use_case = get_settings_by_id_use_case()

        try:
            return use_case.execute(
                user_id=user_id,
                agent_id=agent_id
            )
        
        except (NotFoundException, PermissionsException) as e:
            raise GraphQlException(str(e))
        
        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()