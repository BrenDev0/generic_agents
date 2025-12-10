from pydantic import BaseModel, ConfigDict
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
    email: str
    name:str
    created_at: datetime
    last_login: datetime

class CreateUser(UserShemaBase):
    name: str
    email: str
    password: str

class VerifiedUserUpdate(UserShemaBase):
    email: Optional[str]
    password: Optional[str]

class UpdateUser(UserShemaBase):
    name: Optional[str]
    password: Optional[str]
    old_password: Optional[str]

class Login(UserShemaBase):
    email: str
    password: str