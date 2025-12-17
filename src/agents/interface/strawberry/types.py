import strawberry
from src.agents.domain.schemas import AgentPublic, CreateAgentRequest, UpdatAgentRequest

@strawberry.experimental.pydantic.type(model=AgentPublic, all_fields=True)
class AgentType:
    pass

