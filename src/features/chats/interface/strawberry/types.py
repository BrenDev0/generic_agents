import strawberry
from ...domain import ChatPublic

@strawberry.experimental.pydantic.type(ChatPublic, all_fields=True)
class ChatType:
    pass