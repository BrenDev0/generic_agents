from uuid import UUID
from src.persistence import DataRepository
from ...domain import ChatPublic

class DeleteChat:
    def __init__(
        self,
        chat_repository: DataRepository
    ):
        self.__chat_repository = chat_repository

    def execute(
        self,
        chat_id: UUID
    ):
        
        deleted_chat = self.__chat_repository.delete(
            key="chat_id",
            value=chat_id
        )

        return ChatPublic.model_validate(deleted_chat, from_attributes=True)