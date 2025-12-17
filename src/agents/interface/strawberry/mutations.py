import strawberry
from src.app.interface.strawberry.middleware.user_auth import UserAuth
from src.agents.interface.strawberry.inputs import (
    CreateAgentProfileInput,
    UpdateAgentProfileInput
)

@strawberry.type
class AgentMutation:
    @strawberry.mutation(
        permission_classes=[UserAuth],
        description="Create agent profile"
    )
    def agent_create(
        self,
        info: strawberry.Info,
        input: CreateAgentProfileInput
    ): 
        pass
