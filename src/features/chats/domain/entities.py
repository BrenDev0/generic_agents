from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime

class Chat(BaseModel):
    chat_id: Optional[UUID] = None
    agent_id: UUID
    title: Optional[str] = None
    created_at: Optional[datetime] = None

