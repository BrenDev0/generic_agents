from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from src.features.agents.domain.entities import Agent

class AgentSettings(BaseModel):
    setting_id: Optional[UUID] = None
    agent_id: UUID
    system_prompt: str
    temperature: float
    transcripts: bool = False
    agent: Optional[Agent] = None