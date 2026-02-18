import logging
import strawberry
from uuid import UUID
from src.persistence import NotFoundException
from src.security import PermissionsException
from src.app import GraphQlException
from src.app.interface.strawberry.decorators.req_validation import validate_input_to_model
from src.app.interface.strawberry.middleware.user_auth import UserAuth
from .inputs import CreateAgentSettingsInput, UpdateAgentSettingsInput
from .types import AgentSettingsType
from ...domain import ExistingSettingsException
from ...dependencies import (
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
    @validate_input_to_model
    def create_agent_settings(
        self,
        info: strawberry.Info,
        agent_id: UUID,
        input: CreateAgentSettingsInput
    )-> AgentSettingsType:
        try:
            user_id = info.context.get("user_id")
            use_case = get_agent_settings_create_use_case()

        
            return use_case.execute(
                user_id=user_id,
                agent_id=agent_id,
                settings=input
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
    @validate_input_to_model
    def update_agent_settings(
        self,
        info: strawberry.Info,
        settings_id: UUID,
        input: UpdateAgentSettingsInput
    )-> AgentSettingsType:
        try:
            user_id = info.context.get("user_id")
            use_case = get_agent_settings_update_use_case()

        
            return use_case.execute(
                user_id=user_id,
                settings_id=settings_id,
                changes=input
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
    )-> AgentSettingsType:
        try:
            user_id = info.context.get("user_id")
            use_case = get_agent_settings_delete_use_case()

            return use_case.execute(
                user_id=user_id,
                setting_id=setting_id
            )
            
        except (NotFoundException, PermissionsException) as e:
            raise GraphQlException(str(e))
        
        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()

