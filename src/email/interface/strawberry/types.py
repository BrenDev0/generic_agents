import strawberry
from src.email.domain.schemas import VerifyEmail

@strawberry.experimental.pydantic.type(model=VerifyEmail, all_fields=True)
class VerifyEmailType:
    pass

@strawberry.type
class VerificationTokenType:
    verification_token: str