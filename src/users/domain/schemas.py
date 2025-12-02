from pydantic import BaseModel, ConfigDict, EmailStr
from pydantic.alias_generators import to_camel
from typing import Optional
from datetime import datetime
from uuid import UUID

class UserShemaBase(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        serialize_by_alias=True,
        alias_generator=to_camel,
        extra="forbid"
    )

class UserPublic(UserShemaBase):
    user_id: UUID
    email: EmailStr
    name:str
    created_at: datetime
    last_login: datetime

class CreateUser(UserShemaBase):
    name: str
    email: EmailStr
    password: str

class VerifiedUserUpdate(UserShemaBase):
    email: Optional[EmailStr]
    password: Optional[str]

class UpdateUser(UserShemaBase):
    name: Optional[str]
    password: Optional[str]
    old_password: Optional[str]