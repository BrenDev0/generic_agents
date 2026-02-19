from typing import List
from uuid import UUID
from ...domain import MessageRepository
from ..service import MessageService


class DeleteMessages:
    def __init__(
        self,
        message_repository: MessageRepository,
        message_service: MessageService
    ):
        self.__message_repository = message_repository
        self.__message_service = message_service

    def execute(
        self,
        message_ids: List[UUID]
    ):
        deleted_messages = self.__message_repository.delete_many(
            key="message_id",
            value=message_ids
        )

        return [
            self.__message_service.get_public_schema(message)
            for message in deleted_messages
        ]