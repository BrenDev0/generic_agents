from uuid import UUID
from src.persistence.domain.data_repository import DataRepository
from src.chats.domain.entities import Chat
from src.chats.domain.schemas import ChatPublic


class CreateChat:
    def __init__(
        self,
        repository: DataRepository
    ):
        self.__repository = repository

    def execute(
        self,
        agent_id: UUID
    ):
        data = Chat(
            agent_id=agent_id
        )

        new_chat = self.__repository.create(
            data=data
        )

        return ChatPublic.model_validate(new_chat, from_attributes=True)