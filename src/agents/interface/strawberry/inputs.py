import strawberry
from src.agents.domain.schemas import (
    CreateAgentProfileRequest,
    UpdatAgentProfileRequest
)

@strawberry.experimental.pydantic.input(model=CreateAgentProfileRequest, all_fields=True)
class CreateAgentProfileInput:
    pass

@strawberry.experimental.pydantic.input(model=UpdatAgentProfileRequest, all_fields=True)
class UpdateAgentProfileInput:
    pass