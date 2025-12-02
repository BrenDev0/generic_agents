import strawberry
from uuid import UUID
from src.users.dependencies.use_cases import get_user_use_case
from src.users.interface.strawberry.types import UserType

@strawberry.type
class UserQuery:
    @strawberry.field
    def user(
        self,
        user_id: UUID
    ) -> UserType | None:
        use_case = get_user_use_case()

        return use_case.execute(
            key="user_id",
            value=user_id
        )