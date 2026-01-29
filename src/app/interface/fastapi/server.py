import logging
from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.app.interface.strawberry.router import get_strawberry_graphql_router
from src.app.interface.fastapi.middleware.hmac import verify_hmac
from src.security.domain.exceptions import HMACException

logger = logging.getLogger(__name__)

def create_fastapi_app():
    app = FastAPI()

    # CORS setup
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def catch_request_format_errors(
        req: Request,
        call_next
    ):
        try: 
            return await call_next(req)
        
        except (AttributeError, TypeError, KeyError ,ValueError) as exc:
            logger.error(f"Request parsing error: {str(exc)}", exc_info=True)
            return JSONResponse(
                status_code=400,
                content={
                    "errors": [{
                        "message": "Invalid multipart request format. Check that 'operations' and 'map' fields are correctly formatted.",
                        "extensions": {
                            "code": "INVALID_MULTIPART_REQUEST"
                        }
                    }]
                }
            )
        
    @app.exception_handler(HMACException)
    async def hmac_exception_handler(request, exc: HMACException):
        return JSONResponse(
            status_code=401,
            content={"errors": [exc.detail]}
        )


    @app.exception_handler(Exception)
    async def exception_handler(request, exc: Exception):
        print(str(exc))
        return JSONResponse(
            status_code=500,
            content={"errors": ["Unable to process request  at this time"]}
        )


    @app.get("/", tags=["Internal"])
    async def health():
        """
        ## Health check 
        This endpoints verifies server status.
        """
        return {"status": "ConvertIA ok"}
    
  
    graphql_router = get_strawberry_graphql_router()
    app.include_router(graphql_router, dependencies=[Depends(verify_hmac)])

    return app
    
    