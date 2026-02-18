from uuid import UUID
from src.persistence import DataRepository
from ...domain import Chat, ChatPublic


class CreateChat:
    def __init__(
        self,
        chat_repository: DataRepository
    ):
        self.__chat_repository = chat_repository

    def execute(
        self,
        agent_id: UUID,
        chat_id: UUID
    ):
        data = Chat(
            chat_id=chat_id,
            agent_id=agent_id
        )

        new_chat = self.__chat_repository.create(
            data=data
        )

        return ChatPublic.model_validate(new_chat, from_attributes=True)