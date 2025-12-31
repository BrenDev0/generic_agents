from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from typing import Optional

class ChatBase(BaseModel):
    model_config=ConfigDict(
        serialize_by_alias=True,
        populate_by_name=True,
        str_min_length=1,
        alias_generator=to_camel,
        extra="forbid"
    )

class UpdateChatRequest(BaseModel):
    title: Optional[str] = None
    