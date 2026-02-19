import logging
import strawberry
from typing import List
from src.app import GraphQlException, validate_input_to_model
from src.persistence import NotFoundException
from src.security import StrawberryUserAuth, PermissionsException
from src.features.chats import get_chat_resource_use_case
from ...dependencies import get_delete_messages_use_case
from .types import MessageType
from .inputs import DeleteMessagesInput
logger = logging.getLogger(__name__)

@strawberry.type
class MessageMutaions:
    @strawberry.mutation(
        permission_classes=[StrawberryUserAuth],
        description="Delete Messages"
    )
    @validate_input_to_model
    def delete_messages(
        self,
        input: List[DeleteMessagesInput],
        info: strawberry.Info
    ) -> List[MessageType]:
        try:
            user_id = info.context.get("user_id")
            chat_ids = list(set(message.chat_id for message in input))

            if len(chat_ids) > 1:
                raise GraphQlException("Cannot delete from mutliple chats")
            
            chat_resource_usecase = get_chat_resource_use_case()
            chat_resource_usecase.execute(
                user_id=user_id,
                chat_id=chat_ids[0]
            ) ## will raise permisions error or not found error 

            delete_messages_use_case = get_delete_messages_use_case()
            
            return delete_messages_use_case.execute(
                message_ids=[message.message_id for message in input]
            ) 


        except (NotFoundException, PermissionsException, GraphQlException) as e:
            if isinstance(e, GraphQlException):
                raise 
            raise GraphQlException(str(e))
        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()
