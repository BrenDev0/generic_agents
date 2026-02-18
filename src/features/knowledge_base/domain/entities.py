from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
from src.features.agents import Agent

class Knowledge(BaseModel):
    knowledge_id: Optional[UUID] = None
    agent_id: UUID
    type: str
    size: Optional[str] = None
    name: Optional[str] = None
    description: str
    url: Optional[str] = None
    state: Optional[str] = None
    created_at: Optional[datetime] = None
    agent: Optional[Agent] = None