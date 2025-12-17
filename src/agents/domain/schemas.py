from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from uuid import UUID 
from typing import Optional
from datetime import datetime

class AgentBase(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        serialize_by_alias=True,
        str_min_length=1,
        alias_generator=to_camel,
        extra="forbid"
    )

class AgentPublic(AgentBase):
    agent_id: UUID
    user_id: UUID
    name: str
    description: Optional[str] = None
    created_at: datetime

class CreateAgentProfileRequest(AgentBase):
    name: str
    description: Optional[str] = None

class UpdatAgentProfileRequest(AgentBase):
    name: Optional[str] = None
    description: Optional[str] = None