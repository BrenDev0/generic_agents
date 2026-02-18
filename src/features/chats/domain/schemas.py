from pydantic import BaseModel, ConfigDict
from uuid import UUID
from pydantic.alias_generators import to_camel
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
    created_at: datetime

class CreateChatRequest(ChatBase):
    agent_id: UUID
    chat_id: UUID
