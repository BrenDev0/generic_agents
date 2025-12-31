from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from src.app.interface.strawberry.router import get_strawberry_graphql_router
from src.app.interface.fastapi.middleware.hmac import verify_hmac


def create_fastapi_app():
    app = FastAPI()

    # CORS setup
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:8000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
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
    
    