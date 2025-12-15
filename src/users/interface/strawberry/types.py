import strawberry
from src.users.domain.schemas import UserPublic, CreateUserRequest, LoginRequest, UpdateUserRequest, VerifiedUserUpdateRequest

@strawberry.experimental.pydantic.type(model=UserPublic, all_fields=True)
class UserType:
    pass

@strawberry.type
class UserWithTokenType:
    user: UserType
    token: str

@strawberry.experimental.pydantic.input(model=CreateUserRequest, all_fields=True)
class CreateUserInput:
    pass

@strawberry.experimental.pydantic.input(model=LoginRequest, all_fields=True)
class LoginInput:
    pass

@strawberry.experimental.pydantic.input(model=UpdateUserRequest, all_fields=True)
class UpdateUserInput:
    pass

@strawberry.experimental.pydantic.input(model=VerifiedUserUpdateRequest, all_fields=True)
class VerifiedUserUpdateInput:
    pass
