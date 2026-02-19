from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from uuid import UUID
from datetime import datetime

class MessageConfig(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        serialize_by_alias=True,
        alias_generator=to_camel,
        extra='forbid',
        str_min_length=1
    )

class MessagePublic(MessageConfig):
    message_id: UUID
    chat_id: UUID
    type: str
    text: str
    created_at: datetime

class CreateMessageRequest(BaseModel):
    chat_id: UUID
    type: str
    text: str 
