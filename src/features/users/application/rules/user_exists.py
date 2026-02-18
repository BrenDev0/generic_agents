from src.persistence import NotFoundException, DataRepository
from src.security import HashingService
from ...domain import User

class UserExists:
    def __init__(
        self,
        repository: DataRepository,
        hashing: HashingService
    ):
        self.__user_repository = repository
        self.__hashing = hashing

    def validate(
        self,
        email: str
    ):
        hashed_email = self.__hashing.hash_for_search(data=email)

        user_exists: User = self.__user_repository.get_one(
            key="email_hash",
            value=hashed_email
        )

        if not user_exists:
            raise NotFoundException()
        

        return user_exists