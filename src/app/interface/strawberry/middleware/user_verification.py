import typing
from strawberry.permission import BasePermission
from strawberry.types import Info
from src.security.dependencies.services import get_web_token_service
from src.security.domain.exceptions import ExpiredToken, InvalidToken

class UserVerification(BasePermission):
     message = "Unverified"
     def has_permission(self, source: typing.Any, info: Info, **kwargs) -> bool:
        request = info.context["request"]
       
        authorization = request.headers.get("Authorization") 
        
        if authorization:
            web_token_service = get_web_token_service()
            token = authorization.split("Bearer ")[-1]
            try:
                payload = web_token_service.decode(token)
                verification_code = payload.get("verification_code")
                if verification_code:
                    info.context["verification_code"] = verification_code
                    return True
            
            except ExpiredToken as e:
                self.message = str(e)

            except InvalidToken as e:
                self.message = str(e)

            except Exception:
                return False
            
        return False