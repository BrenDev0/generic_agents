import strawberry
from ...domain import VerifyEmail

@strawberry.experimental.pydantic.input(model=VerifyEmail, all_fields=True)
class VerifyEmailType:
    pass

@strawberry.type
class VerificationTokenType:
    verification_token: str

@strawberry.type
class EmailConfirmationType:
    message: str