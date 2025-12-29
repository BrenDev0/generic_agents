from uuid import UUID
from src.shared.domain.repositories.data_repository import DataRepository


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
        pass