import strawberry
import logging
from uuid import UUID
from typing import List, Optional
from src.app import GraphQlException
from src.security import StrawberryUserAuth
from src.security import PermissionsException
from ...dependencies import get_chat_collection_use_case
from .types import ChatType
logger = logging.getLogger(__name__)


@strawberry.type
class ChatQueries:
    @strawberry.field(
        permission_classes=[StrawberryUserAuth],
        description="get chats by agent id"
    )
    def chat_collection(
        self,
        info: strawberry.Info,
        agent_id: UUID,
        page_number: int,
        per_page: Optional[int] = 10
    ) -> List[ChatType]:
        try:
            user_id = info.context.get("user_id")
            use_case = get_chat_collection_use_case()

            return use_case.execute(
                user_id=user_id,
                agent_id=agent_id,
                page_number=page_number,
                per_page=per_page
            )

        except PermissionsException as e:
            raise GraphQlException(str(e))
        
        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()