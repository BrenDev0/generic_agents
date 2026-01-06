from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
from src.features.agents.domain.entities import Agent

class Knowledge(BaseModel):
    knowledge_id: Optional[UUID] = None
    agent_id: UUID
    type: str
    name: Optional[str] = None
    description: str
    url: Optional[str] = None
    is_embedded: Optional[bool] = False
    created_at: Optional[datetime] = None
    agent: Optional[Agent] = None