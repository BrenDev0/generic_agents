from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from src.app.setup.startup import startup_event

from src.app.interface.strawberry.router import get_strawberry_graphql_router


def create_fastapi_app():
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        startup_event()
        yield

    app = FastAPI(lifespan=lifespan)

    # CORS setup
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:8000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    

    @app.get("/health", tags=["Internal"])
    async def health():
        """
        ## Health check 
        This endpoints verifies server status.
        """
        return {"status": "ok"}
    

    graphql_router = get_strawberry_graphql_router()
    app.include_router(graphql_router)

    return app
    
    