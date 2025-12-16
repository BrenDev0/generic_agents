from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class Agent(BaseModel):
    agent_id: UUID
    user_id: UUID
    name: str
    description: str
    created_at: datetime