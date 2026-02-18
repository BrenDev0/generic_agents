import strawberry
from ...domain import CreateSettingsRequest, UpdateSettingsRequest

@strawberry.experimental.pydantic.input(model=CreateSettingsRequest, all_fields=True)
class CreateAgentSettingsInput:
    pass

@strawberry.experimental.pydantic.input(model=UpdateSettingsRequest, all_fields=True)
class UpdateAgentSettingsInput:
    pass