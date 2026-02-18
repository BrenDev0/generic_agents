from datetime import datetime, timezone
from src.persistence import DataRepository, NotFoundException
from src.security import HashingService, EncryptionService
from ...domain import User, UserPublic


class UserLogin:
    def __init__(
        self,
        repository: DataRepository,
        hashing: HashingService,
        encryption: EncryptionService
    ) -> UserPublic:
        self.__repository = repository
        self.__hashing = hashing
        self.__encrytpion = encryption

    
    def execute(
        self,
        email: str,
        password: str
    ):
        
        hashed_email = self.__hashing.hash_for_search(email)

        user_exists: User | None = self.__repository.get_one(
            key="email_hash",
            value=hashed_email
        )

        if not user_exists:
            raise NotFoundException()

        self.__hashing.compare_password(
            password=password,
            hashed_password=user_exists.password,
            detail="Incorrect email or password",
            throw_error=True
        )

        ## Update last login
        changes = {
            "last_login": datetime.now(timezone.utc)
        }

        updated_user: User = self.__repository.update(
            key="user_id",
            value=user_exists.user_id,
            changes=changes
        )

        user_public = UserPublic(
            user_id=user_exists.user_id,
            email=self.__encrytpion.decrypt(updated_user.email),
            name=self.__encrytpion.decrypt(updated_user.name),
            last_login=updated_user.last_login,
            created_at=updated_user.created_at
        )

        return user_public