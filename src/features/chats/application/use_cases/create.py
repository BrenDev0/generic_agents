from uuid import UUID
from src.persistence import DataRepository
from ...domain import Chat, ChatPublic


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