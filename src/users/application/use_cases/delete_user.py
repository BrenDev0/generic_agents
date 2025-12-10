from uuid import UUID
from src.shared.domain.repositories.data_repository import DataRepository

class DeleteUser:
    def __init__(
        self,
        repository: DataRepository
    ):
        self.__repository = repository

    def execute(
        self,
        user_id: UUID
    ):
        return self.__repository.delete(
            key="user_id",
            value=user_id
        )