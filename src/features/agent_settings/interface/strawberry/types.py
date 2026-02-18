import strawberry
from ...domain import AgentSettingsPublic

@strawberry.experimental.pydantic.type(model=AgentSettingsPublic, all_fields=True)
class AgentSettingsType:
    pass