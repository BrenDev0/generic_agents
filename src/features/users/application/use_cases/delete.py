from uuid import UUID
from src.security import EncryptionService
from src.persistence import DataRepository, NotFoundException
from ...domain import User, UserPublic

class DeleteUser:
    def __init__(
       self,
        repository: DataRepository,
        encryption: EncryptionService
    ) -> UserPublic:
        self.__repository = repository
        self.__encryption = encryption


    def execute(
        self,
        user_id: UUID
    ):
        deleted_user: User =  self.__repository.delete(
            key="user_id",
            value=user_id
        )

        if not deleted_user:
            raise NotFoundException()

        return UserPublic(
            user_id=deleted_user.user_id,
            email=self.__encryption.decrypt(deleted_user.email),
            name=self.__encryption.decrypt(deleted_user.name),
            created_at=deleted_user.created_at,
            last_login=deleted_user.last_login
        ) 