import strawberry
from src.features.agents.domain.schemas import AgentPublic

@strawberry.experimental.pydantic.type(model=AgentPublic, all_fields=True)
class AgentType:
    pass

