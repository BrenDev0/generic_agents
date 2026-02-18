from uuid import UUID
from typing import List
from src.persistence import DataRepository
from src.security import PermissionsException
from ...domain import Chat, ChatPublic

class GetChatsCollection:
    def __init__(
        self,
        chat_repository: DataRepository
    ):
        self.__chat_repository = chat_repository

    def execute(
        self,
        user_id: UUID,
        agent_id: UUID,
        page_number: int,
        per_page: int = 10,  
    ):
        offset = (page_number - 1) * per_page
        chats: List[Chat] = self.__chat_repository.get_many(
            key="agent_id",
            value=agent_id,
            limit=per_page,
            offset=offset
        )

        if not chats:
            return []

        if str(user_id) != str(chats[0].agent.user_id):
            raise PermissionsException()

        return [
            ChatPublic.model_validate(chat, from_attributes=True)
            for chat in chats
        ] 