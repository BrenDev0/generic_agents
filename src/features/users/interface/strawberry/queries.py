import logging
import strawberry
from src.app.domain import GraphQlException
from src.security import StrawberryUserAuth
from ...dependencies import get_user_use_case
from .types import UserType
logger = logging.getLogger(__name__)

@strawberry.type
class UserQueries:
    @strawberry.field(
        permission_classes=[StrawberryUserAuth],
        description="Get User from id in Auth token"
    )
    def get_me(
        self,
        info: strawberry.Info
    ) -> UserType | None:
        try:
            use_case = get_user_use_case()

            user_id = info.context.get("user_id")
            
            return use_case.execute(
                key="user_id",
                value=user_id
            )

        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()