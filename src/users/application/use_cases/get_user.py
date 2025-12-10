from src.shared.domain.repositories.data_repository import DataRepository
from src.security.domain.services.encryption_service import EncryptionService
from src.users.domain.schemas import UserPublic
from src.users.domain.entities import User

class GetUser:
    def __init__(
        self,
        repository: DataRepository,
        encryption: EncryptionService
    ):
        self.__repository = repository
        self.__encryption = encryption

    def execute(
        self,
        key: str,
        value: str
    ) -> UserPublic | None:
        user: User = self.__repository.get_one(
            key=key,
            value=value
        )

        if user:
            return UserPublic(
                user_id=user.user_id,
                email=self.__encryption.decrypt(user.email),
                name=self.__encryption.decrypt(user.name),
                last_login=user.last_login,
                created_at=user.created_at
            )

        return None
    

