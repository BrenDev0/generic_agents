from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from typing import Optional
from uuid import UUID

class AgentSettingsBase(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        serialize_by_alias=True,
        str_min_length=1,
        alias_generator=to_camel,
        extra="forbid"
    )


class CreateSettingsRequest(AgentSettingsBase):
    system_prompt: str
    temperature: float
    transcripts: bool

class AgentSettingsPublic(CreateSettingsRequest):
    setting_id: UUID


class UpdateSettingsRequest(AgentSettingsBase):
    system_prompt: Optional[str] = None
    temperature: Optional[str] = None
    transcripts: Optional[bool] = None

