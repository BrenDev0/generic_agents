import logging
import strawberry
from src.app import GraphQlException, validate_input_to_model
from src.persistence import NotFoundException, UpdateFieldsException
from src.security import (
    IncorrectPassword, 
    get_web_token_service, 
    get_encrytpion_service,
    StrawberryUserAuth,
    StrawberryUserVerification
)
from src.features.knowledge_base import get_delete_knowledge_by_user_use_case
from .inputs import CreateUserInput, UpdateUserInput, LoginInput, VerifiedLoginInput, VerifiedUserUpdateInput
from .types import UserType, UserWithTokenType, TokenType
from ...domain import UpdateUserSchema
from ...dependencies import use_cases, business_rules

logger = logging.getLogger(__name__)

@strawberry.type
class UserMutations:
    @strawberry.mutation(
        permission_classes=[StrawberryUserVerification],
        description="Verification token from verify email must be used as Auth Bearer."
    )
    @validate_input_to_model
    def create_user(
        self,
        info: strawberry.Info,
        input: CreateUserInput
    ) -> UserWithTokenType:
        try:
            use_case = use_cases.get_create_user_use_case()
            web_token_service = get_web_token_service()

            verification_code = info.context.get("verification_code")
            encryption = get_encrytpion_service()

            if int(input.code) != int(encryption.decrypt(verification_code)):
                raise GraphQlException("401")
            
            new_user = use_case.execute(
                name=input.name,
                email=input.email,
                password=input.password
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
            raise GraphQlException()
    
    @strawberry.mutation(
        permission_classes=[StrawberryUserAuth],
        description="Update user by user id in auth token"
    )
    @validate_input_to_model
    def update_user(
        self,
        info: strawberry.Info,
        input: UpdateUserInput
    ) -> UserType:
        try:
            use_case = use_cases.get_update_user_use_case()
        
            user_id = info.context.get("user_id")
            changes = {}
       
            if input.password:
                if not input.old_password:
                    raise GraphQlException("Old password requiered to update password")
            
                rule = business_rules.get_update_password_rule()
                rule.validate(
                    user_id=user_id,
                    new_password=input.password,
                    old_password=input.old_password,
                    current_password_check=True
                )

                changes["password"] = input.password

            if input.name is not None:
                changes["name"] = input.name

            return use_case.execute(
                user_id=user_id,
                changes=UpdateUserSchema(**changes)
            )
            
        except (NotFoundException, IncorrectPassword) as e:
            raise GraphQlException(str(e))
           
        except GraphQlException:
            raise

        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()
        
    
    @strawberry.mutation(
        description="Update email, or password for account recovery",
        permission_classes=[StrawberryUserVerification]
    )
    @validate_input_to_model
    def verified_update(
        self,
        info: strawberry.Info,
        input: VerifiedUserUpdateInput
    ) -> UserType:
        user_id = info.context.get("user_id")
        if not user_id:
            raise GraphQlException("403")
            
        verification_code = info.context.get("verification_code")
        encryption = get_encrytpion_service()
        
        if int(input.code) != int(encryption.decrypt(verification_code)):
            raise GraphQlException("401")
        
        if input.email and input.password:
            raise GraphQlException("Cannot update email and password simultaneously")
        
        try:    
            use_case = use_cases.get_update_user_use_case()
            if input.password:
                rule = business_rules.get_update_password_rule()

                rule.validate(
                    user_id=user_id,
                    new_password=input.password,
                    current_password_check=False
                )

            changes = UpdateUserSchema(
                **input.model_dump(exclude_none=True, exclude={"code"})
            )

            return use_case.execute(
                user_id=user_id,
                changes=changes
            )
        
        except (NotFoundException, IncorrectPassword, UpdateFieldsException) as e:
            raise GraphQlException(str(e))

        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()

    @strawberry.mutation(
        description="User login"
    )
    @validate_input_to_model
    def login(
        self,
        input: LoginInput
    ) -> UserWithTokenType:
        try:
            use_case = use_cases.get_login_use_case()
            web_token_service = get_web_token_service()

            user = use_case.execute(
                email=input.email,
                password=input.password
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
            raise GraphQlException("400")

        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()
        

    @strawberry.mutation(
        permission_classes=[StrawberryUserAuth],
        description="Delete user by id in auth token"
    )
    async def delete_user(
        self,
        info: strawberry.Info
    ) -> UserType:
        try:
            use_case = use_cases.get_delete_user_use_case()
            user_id = info.context.get("user_id")
            delete_uploads_use_case = get_delete_knowledge_by_user_use_case()

            await delete_uploads_use_case.execute(
                user_id=user_id
            )

            return use_case.execute(
                user_id=user_id
            )

        except NotFoundException as e:
            raise GraphQlException(str(e))
        
        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()

    @strawberry.mutation(
        permission_classes=[StrawberryUserVerification],
        description="login in with code from  email"
    )
    @validate_input_to_model
    def verified_login(
        self,
        info: strawberry.Info,
        input: VerifiedLoginInput
    ) -> TokenType:
        user_id = info.context.get("user_id")
        if not user_id:
            
            raise GraphQlException("403")
            
        verification_code = info.context.get("verification_code")
        encryption = get_encrytpion_service()
        
        if int(input.verification_code) != int(encryption.decrypt(verification_code)):
            raise GraphQlException("401")
        
        try:
            service = get_web_token_service()

            token_payload = {
                "user_id": str(user_id)
            }

            token = service.generate(payload=token_payload, expiration=900)

            return TokenType(
                token=token
            )

        except Exception as e: 
            logger.error(str(e))
            raise GraphQlException()    
        

            

