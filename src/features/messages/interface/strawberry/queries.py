import strawberry
import logging
from uuid import UUID
from typing import List, Optional
from src.app import GraphQlException
from src.persistence import NotFoundException
from src.security import StrawberryUserAuth, PermissionsException
from src.features.chats import get_chat_resource_use_case
from ...dependencies import get_messages_collection_use_case
from .types import MessageType
logger = logging.getLogger(__name__)


@strawberry.type
class MessageQueries:
    @strawberry.field(
        permission_classes=[StrawberryUserAuth],
        description="get messages by chat id"
    )
    def message_collection(
        self,
        info: strawberry.Info,
        chat_id: UUID,
        page_number: int,
        per_page: Optional[int] = 10,
        
    ) -> List[MessageType]:
        if page_number < 1:
                raise GraphQlException("Page cannot be 0")
        try:
            user_id = info.context.get("user_id")
            chat_resource_use_case = get_chat_resource_use_case()

            chat_resource_use_case.execute(
                user_id=user_id,
                chat_id=chat_id
            ) # check permissions and if chat exists

            message_collection_use_case = get_messages_collection_use_case()
            return message_collection_use_case.execute(
                chat_id=chat_id,
                page_number=page_number,
                per_page=per_page
            )
            
        except (NotFoundException, PermissionsException) as e:
            raise GraphQlException(str(e))
        
        except Exception as e: 
            logger.error(str(e))
            raise GraphQlException()
