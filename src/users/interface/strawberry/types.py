import strawberry
from src.users.domain.schemas import UserPublic

@strawberry.experimental.pydantic.type(model=UserPublic, all_fields=True)
class UserType:
    pass