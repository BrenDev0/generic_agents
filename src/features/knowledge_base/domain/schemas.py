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
    size: str | None
    name: str
    description: str
    url: str
    state: str
    created_at: datetime

class CreateKnowledgeRequest(KnowledgeConfig):
    description: str
    state: Optional[str] = None
    connection_id: Optional[UUID] = None

class UpdateKnowledgeRequest(KnowledgeConfig):
    name: Optional[str] = None
    description: Optional[str] = None
    state: str

class InternalUpdateEmbeddingStatus(BaseModel):
    user_id: UUID
    status: bool
