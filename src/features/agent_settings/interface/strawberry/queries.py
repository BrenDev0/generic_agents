import strawberry
import logging
from uuid import UUID
from src.features.agent_settings.dependencies.use_cases import get_settings_by_id_use_case
from src.features.agent_settings.interface.strawberry.types import AgentSettingsType
from src.app.domain.exceptions import GraphQlException
from src.app.interface.strawberry.middleware.user_auth import UserAuth 
from src.security.domain.exceptions import PermissionsException
from src.persistence.domain.exceptions import NotFoundException


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
        try:        
            user_id = info.context.get("user_id")
            use_case = get_settings_by_id_use_case()

            return use_case.execute(
                user_id=user_id,
                agent_id=agent_id
            )
        
        except (NotFoundException, PermissionsException) as e:
            raise GraphQlException(str(e))
        
        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()