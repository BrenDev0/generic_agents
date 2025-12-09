import logging
import strawberry
from uuid import UUID
from src.users.dependencies.use_cases import get_user_use_case
from src.users.interface.strawberry.types import UserType
from src.app.interface.strawberry.context import Context
from src.shared.domain.exceptions.graphql import GraphQlException
from src.app.middleware.auth import UserAuth
logger = logging.getLogger(__name__)

@strawberry.type
class UserQuery:
    @strawberry.field(permission_classes=[UserAuth])
    def user(
        self,
        info: strawberry.Info[Context]
    ) -> UserType | None:
        try:
            user_id = info.context[user_id]
            logger.debug(f"USERID:::: {user_id}")
            use_case = get_user_use_case()
        
            return use_case.execute(
                key="user_id",
                value=user_id
            )

        except GraphQlException as e:
            return e.to_dict()