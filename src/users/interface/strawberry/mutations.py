import logging
import strawberry
from src.users.interface.strawberry.types import UserType, CreateUserInput, UserWithTokenType
from src.shared.domain.exceptions.graphql import GraphQlException
from src.users.dependencies.use_cases import get_create_user_use_case
from src.security.dependencies.services import get_web_token_service
logger = logging.getLogger(__name__)

@strawberry.type
class UserMutation:
    @strawberry.field
    def create_user(
        data: CreateUserInput
    ) -> UserWithTokenType:
        use_case = get_create_user_use_case()
        web_token_service = get_web_token_service()
       
        try:
            new_user = use_case.execute(
                name=data.name,
                email=data.email,
                password=data.password
            )

            token_payload = {
                "user_id": str(new_user.user_id)
            }

            token = web_token_service.generate(
                payload=token_payload,
                expiration=604800 # 7 days
            )

            
            return UserWithTokenType(
                user=new_user,
                token=token
            )

        except Exception as e:
            logger.error(str(e))
            raise GraphQlException("Unable to process request at this time")


