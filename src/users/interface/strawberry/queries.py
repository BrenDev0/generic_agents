import logging
import strawberry
from uuid import UUID
from src.users.dependencies.use_cases import get_user_use_case
from src.users.interface.strawberry.types import UserType
from src.app.interface.strawberry.context import Context
logger = logging.getLogger(__name__)

@strawberry.type
class UserQuery:
    @strawberry.field
    def user(
        self,
        info: strawberry.Info[Context]
    ) -> UserType | None:
        user_id = info.context.user_id
        use_case = get_user_use_case()
      
        return use_case.execute(
            key="user_id",
            value=user_id
        )