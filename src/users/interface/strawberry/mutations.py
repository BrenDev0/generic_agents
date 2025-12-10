import logging
import strawberry
from src.app.interface.strawberry.middleware.user_auth import UserAuth
from src.users.interface.strawberry.types import UserType, CreateUserInput, UserWithTokenType, LoginInput
from src.shared.domain.exceptions.graphql import GraphQlException
from src.shared.domain.exceptions.repositories import NotFoundException
from src.security.domain.exceptions import IncorrectPassword
from src.users.dependencies.use_cases import get_create_user_use_case, get_login_use_case, get_delete_user_use_case
from src.security.dependencies.services import get_web_token_service
logger = logging.getLogger(__name__)

@strawberry.type
class UserMutation:
    @strawberry.field
    def create_user(
        self,
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
    
    @strawberry.field
    def login(
        self,
        data: LoginInput
    ) -> UserWithTokenType:
        use_case = get_login_use_case()
        web_token_service = get_web_token_service()

        try:
            user = use_case.execute(
                email=data.email,
                password=data.password
            )
            token_payload = {
                "user_id": str(user.user_id)
            }

            token = web_token_service.generate(
                payload=token_payload,
                expiration=604800 # 7 days
            )

            return UserWithTokenType(
                user=user,
                token=token
            )
        
        except (NotFoundException, IncorrectPassword):
            raise GraphQlException("Incorrect email or password")

        except Exception:
            raise GraphQlException()
        

    @strawberry.field(permission_classes=[UserAuth])
    def delete_user(
        self,
        info: strawberry.Info
    ) -> None:
        use_case = get_delete_user_use_case()
        try:
            user_id = info.context.get("user_id")
            use_case.execute(
                user_id=user_id
            )

            return
        except Exception:
            raise GraphQlException()


