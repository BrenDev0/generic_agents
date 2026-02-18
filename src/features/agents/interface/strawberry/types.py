import strawberry
from ...domain import AgentPublic

@strawberry.experimental.pydantic.type(model=AgentPublic, all_fields=True)
class AgentType:
    pass

