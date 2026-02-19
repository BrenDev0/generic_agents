import strawberry
from ...domain import MessagePublic

@strawberry.experimental.pydantic.input(MessagePublic, all_fields=True)
class DeleteMessagesInput:
    pass