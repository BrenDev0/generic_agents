from pydantic import BaseModel
from uuid import UUID
from typing import Optional 
from datetime import datetime


class Message(BaseModel):
    message_id: Optional[UUID] = None
    chat_id: UUID
    type: str
    text: str
    created_at: Optional[datetime] = None