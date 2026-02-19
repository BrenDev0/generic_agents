from uuid import UUID
from src.persistence import DataRepository, NotFoundException
from src.security import PermissionsException
from ...domain import Chat

class GetChatResource:
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
        
        if str(user_id) !=  str(chat.agent.user_id):
            raise PermissionsException()
        
        return chat