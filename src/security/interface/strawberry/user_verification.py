import typing
from strawberry.permission import BasePermission
from strawberry.types import Info
from src.security import (
    get_web_token_service, 
    ExpiredToken, 
    InvalidToken
)
from src.app import GraphQlException

class UserVerification(BasePermission):
     message = "401"
     def has_permission(self, source: typing.Any, info: Info, **kwargs) -> bool:
        request = info.context["request"]
       
        authorization = request.headers.get("Authorization") 
        
        if authorization:
            web_token_service = get_web_token_service()
            token = authorization.split("Bearer ")[-1]
            try:
                payload = web_token_service.decode(token)
                verification_code = payload.get("verification_code")
                user_id = payload.get("user_id")

                if user_id:
                    info.context["user_id"] = user_id
                    
                if verification_code:
                    info.context["verification_code"] = verification_code
                    return True
            
            except ExpiredToken as e:
                self.message = str(e)

            except InvalidToken as e:
                self.message = str(e)

            except Exception:
                raise GraphQlException()
            
        raise GraphQlException(self.message)