import logging
from functools import cached_property
from typing import Optional
from strawberry.fastapi import BaseContext
from src.security.dependencies.services import get_web_token_service
from src.security.domain.exceptions import ExpiredToken, InvalidToken
from src.shared.domain.exceptions.graphql import GraphQlException
logger = logging.getLogger(__name__)

class Context(BaseContext):
    @cached_property
    def user_id(self) -> Optional[str]:
        if not self.request:
            return None
        
        auth = self.request.headers.get("Authorization")
        if not auth or not auth.startswith("Bearer "):
            return None
        
        token = auth.split(" ")[1]
        logger.debug(f"token :::{token}")
        token_service = get_web_token_service()
        
        try:
            payload = token_service.decode(token)
            logger.debug(f"payload ::: {payload}")
            return payload.get("user_id")
        
        except ExpiredToken:
            raise GraphQlException("Token Expired")
        
        except InvalidToken:
            raise GraphQlException("Invalid Token")
        except Exception:
            return None


def get_context() -> Context:
    return Context()