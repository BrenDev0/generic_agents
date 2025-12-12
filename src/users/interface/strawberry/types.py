import strawberry
from src.users.domain.schemas import UserPublic, CreateUser, Login

@strawberry.experimental.pydantic.type(model=UserPublic, all_fields=True)
class UserType:
    pass

@strawberry.type
class UserWithTokenType:
    user: UserType
    token: str

@strawberry.experimental.pydantic.input(model=CreateUser, all_fields=True)
class CreateUserInput:
    pass

@strawberry.experimental.pydantic.input(model=Login, all_fields=True)
class LoginInput:
    pass

