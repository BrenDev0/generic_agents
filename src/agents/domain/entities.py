from pydantic import BaseModel
from uuid import UUID
class Agent(BaseModel):
    agent_id: UUID
    user_id: UUID
    name: str
    description: str