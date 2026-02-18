from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class User(BaseModel):
    user_id: Optional[UUID] = None
    name: str
    email: str
    email_hash: str
    password: str
    created_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
