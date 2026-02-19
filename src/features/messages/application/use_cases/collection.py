from uuid import UUID
from ...domain import MessageRepository
from ..service import MessageService

class GetMessageCollection:
    def __init__(
        self,
        message_repository: MessageRepository,
        message_service: MessageService
    ):
        self.__message_repository = message_repository
        self.__message_service = message_service

    def execute(
        self,
        chat_id: UUID,
        page_number: int,
        per_page: int
    ):
        offset = (page_number -1) * per_page

        messages = self.__message_repository.get_many(
            key="chat_id",
            value=chat_id,
            limit=per_page,
            offset=offset
        )

        return [
            self.__message_service.get_public_schema(message)
            for message in messages
        ] if messages else []
        
