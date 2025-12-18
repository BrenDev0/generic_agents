from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class AgentSetting(BaseModel):
    setting_id: Optional[UUID] = None
    system_prompt: str
    tempurature: float
    transcripts: bool = False