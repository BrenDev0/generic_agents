from  pydantic import BaseModel


class Email(BaseModel):
    from_: str
    to: str
    subject: str
    html: str
