import strawberry
from ...domain import MessagePublic

@strawberry.experimental.pydantic.type(MessagePublic, all_fields=True)
class MessageType:
    pass