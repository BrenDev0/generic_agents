from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime
from src.features.agents import Agent

class Chat(BaseModel):
    chat_id: UUID
    agent_id: UUID
    created_at: Optional[datetime] = None
    agent: Optional[Agent] = None

