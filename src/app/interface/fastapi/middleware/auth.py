from fastapi import Request, HTTPException, Depends
from src.security.domain.exceptions import ExpiredToken, InvalidToken
from src.security.domain.services.web_token import WebTokenService
from src.security.dependencies.services import get_web_token_service

def auth_middleware(
    request: Request,
    web_token_service: WebTokenService = Depends(get_web_token_service)
):
    auth_header = request.headers.get("Authorization", None)
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unautrhorized, Missing required auth headers")

    token = auth_header.split(" ")[1]

    try:
        token_payload = web_token_service.decode(token)
        user_id = token_payload.get("user_id", None)

        if not user_id:
            raise InvalidToken()
        
        request.state.user = user_id
    
    except ExpiredToken:
        raise HTTPException(status_code=403, detail="Expired Token")
    
    except InvalidToken:
         raise HTTPException(status_code=401, detail="Invalid token")
    
    except ValueError as e:
            raise HTTPException(status_code=401, detail=str(e))