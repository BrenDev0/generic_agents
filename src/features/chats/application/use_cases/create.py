from uuid import UUID
from src.persistence.domain import data_repository, exceptions
from src.features.chats.domain import entities, schemas


class CreateChat:
    def __init__(
        self,
        repository: data_repository.DataRepository
    ):
        self.__repository = repository

    def execute(
        self,
        agent_id: UUID
    ):
        data = entities.Chat(
            agent_id=agent_id
        )

        new_chat = self.__repository.create(
            data=data
        )

        return schemas.ChatPublic.model_validate(new_chat, from_attributes=True)