from src.shared.domain.repositories.data_repository import DataRepository
from src.users.domain.schemas import CreateUser, UserPublic
from src.users.domain.entities import User

class CreateUser:
    def __init__(
        self,
        repository: DataRepository
    ):
        self.__repository = repository

    
    def execute(
        self,
        name: str,
        email: str,
        password: str
    ):
        
        email_hash = "hash_test"
        user = User(
            name=name,
            email=email,
            password=password,
            email_hash=email_hash
        )


        new_user = self.__repository.create(data=user)

        return UserPublic.model_validate(new_user, from_attributes=True)