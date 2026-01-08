import logging
import strawberry
from uuid import UUID
from src.persistence.domain.exceptions import NotFoundException
from src.security.domain.exceptions import PermissionsException
from src.app.domain.exceptions import GraphQlException
from src.app.interface.strawberry.middleware.user_auth import UserAuth
from src.features.agent_settings.interface.strawberry import inputs, types
from src.features.agent_settings.domain.exceptions import ExistingSettingsException
from src.features.agent_settings.dependencies.use_cases import (
    get_agent_settings_create_use_case,
    get_agent_settings_delete_use_case,
    get_agent_settings_update_use_case
)

logger = logging.getLogger(__name__)

@strawberry.type
class AgentSettingsMutations:
    @strawberry.field(
        description="Create settings for an agent",
        permission_classes=[UserAuth]
    )
    def create_agent_settings(
        self,
        info: strawberry.Info,
        agent_id: UUID,
        input: inputs.CreateAgentSettingsInput
    )-> types.AgentSettingsType:
        user_id = info.context.get("user_id")
        use_case = get_agent_settings_create_use_case()

        try:
            return use_case.execute(
                user_id=user_id,
                agent_id=agent_id,
                settings=input.to_pydantic()
            )
            
        except (NotFoundException, PermissionsException, ExistingSettingsException) as e:
            raise GraphQlException(str(e))
        
        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()
        
    
    @strawberry.field(
        description="Update settings for an agent",
        permission_classes=[UserAuth]
    )
    def update_agent_settings(
        self,
        info: strawberry.Info,
        settings_id: UUID,
        input: inputs.UpdateAgentSettingsInput
    )-> types.AgentSettingsType:
        user_id = info.context.get("user_id")
        use_case = get_agent_settings_update_use_case()

        try:
            return use_case.execute(
                user_id=user_id,
                settings_id=settings_id,
                changes=input.to_pydantic()
            )
            
        except (NotFoundException, PermissionsException) as e:
            raise GraphQlException(str(e))
        
        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()
        
    
    @strawberry.field(
        description="Delete settings for an agent",
        permission_classes=[UserAuth]
    )
    def delete_agent_settings(
        self,
        info: strawberry.Info,
        setting_id: UUID
    )-> types.AgentSettingsType:
        user_id = info.context.get("user_id")
        use_case = get_agent_settings_delete_use_case()

        try:
            return use_case.execute(
                user_id=user_id,
                setting_id=setting_id
            )
            
        except (NotFoundException, PermissionsException) as e:
            raise GraphQlException(str(e))
        
        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()

