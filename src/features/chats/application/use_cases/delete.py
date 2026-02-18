from uuid import UUID
from src.persistence import DataRepository, NotFoundException
from src.security import PermissionsException
from ...domain import ChatPublic, Chat

class DeleteChat:
    def __init__(
        self,
        chat_repository: DataRepository
    ):
        self.__chat_repository = chat_repository

    def execute(
        self,
        user_id: UUID,
        chat_id: UUID
    ):
        chat: Chat = self.__chat_repository.get_one(
            key="chat_id",
            value=chat_id
        )

        if not chat:
            raise NotFoundException()
        
        if str(user_id) != str(chat.agent.user_id):
            raise PermissionsException()
        
        deleted_chat = self.__chat_repository.delete(
            key="chat_id",
            value=chat_id
        )

        return ChatPublic.model_validate(deleted_chat, from_attributes=True)