import strawberry
import logging
from uuid import UUID
from src.app import GraphQlException, validate_input_to_model
from src.security import StrawberryUserAuth, PermissionsException
from src.persistence import NotFoundException
from ...dependencies import (
    get_delete_chat_use_case
)
logger = logging.getLogger(__name__)

@strawberry.type
class ChatMutations:
    @strawberry.mutation(
        description="Delete chat",
        permission_classes=[StrawberryUserAuth]
    )
    @validate_input_to_model
    def delete_chat(
        self, 
        chat_id: UUID,
        info: strawberry.Info,
    ):
        try:
            user_id = info.context.get("user_id")   
            use_case = get_delete_chat_use_case()

            return use_case.execute(
                user_id=user_id,
                chat_id=chat_id
            )
        
        except (PermissionsException, NotFoundException) as e:
            raise GraphQlException(str(e))

        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()