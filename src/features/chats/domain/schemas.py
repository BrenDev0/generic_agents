from pydantic import BaseModel, ConfigDict
from uuid import UUID
from pydantic.alias_generators import to_camel
from typing import Optional
from datetime import datetime

class ChatBase(BaseModel):
    model_config=ConfigDict(
        serialize_by_alias=True,
        populate_by_name=True,
        str_min_length=1,
        alias_generator=to_camel,
        extra="forbid"
    )

class ChatPublic(ChatBase):
    chat_id: UUID
    agent_id: UUID
    title: Optional[str] = None
    created_at: datetime

class UpdateChatRequest(BaseModel):
    title: Optional[str] = None
    