from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from typing import Optional
from uuid import UUID
from datetime import datetime

class KnowledgeConfig(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        serialize_by_alias=True,
        alias_generator=to_camel,
        extra="forbid",
        str_min_length=1
    )

class KnowledgePublic(KnowledgeConfig):
    knowledge_id: UUID
    agent_id: UUID
    type: str
    name: str
    description: str
    url: str
    is_embedded: bool
    created_at: datetime

class CreateKnowledgeRequest(KnowledgeConfig):
    description: str

class UpdateKnowledgeRequest(KnowledgeConfig):
    name: Optional[str] = None
    description: Optional[str] = None