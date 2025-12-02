from uuid import UUID 
from src.shared.domain.repositories.data_repository import DataRepository
from src.users.domain.schemas import UserPublic

class GetUser:
    def __init__(
        self,
        repository: DataRepository
    ):
        self.__repository = repository

    def execute(
        self,
        key: str,
        value: str
    ) -> UserPublic | None:
        user = self.__repository.get_one(
            key=key,
            value=value
        )

        if user:
            return UserPublic.model_validate(user, from_attributes=True)

        return None
    

