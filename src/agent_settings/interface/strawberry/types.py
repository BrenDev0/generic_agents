import strawberry
from src.agent_settings.domain.schemas  import AgentSettingsPublic

@strawberry.experimental.pydantic.type(model=AgentSettingsPublic, all_fields=True)
class AgentSettingsType:
    pass