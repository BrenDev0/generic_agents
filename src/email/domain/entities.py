from  pydantic import BaseModel, Field


class Email(BaseModel):
    from_: str = Field(alias="from")
    to: str
    subject: str
    html: str
