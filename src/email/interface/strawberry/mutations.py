import logging
import strawberry
from src.email.interface.strawberry.types import VerificationTokenType, VerifyEmailType

@strawberry.field
class EmailMutation:
    @strawberry.field
    def verify_email(
        self,
        data: VerifyEmailType
    ) -> VerificationTokenType:
        pass