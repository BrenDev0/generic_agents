import strawberry
from uuid import UUID
from src.app.interface.strawberry.middleware.user_auth import UserAuth

@strawberry.type
class AgentQueries:
    @strawberry.field(
        permission_classes=[UserAuth],
        description="Get Agent by id"
    )
    def get_agent(
        self,
        info: strawberry.Info,
        agent_id: UUID
    ):
        pass