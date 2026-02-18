from uuid import UUID
from src.persistence import DataRepository, NotFoundException
from src.security import HashingService, IncorrectPassword
from src.features.users.domain.entities import User


class UpdatePasswordRule:
    def __init__(
        self,
        repository: DataRepository,
        hashing: HashingService
    ):
        self.__repository = repository
        self.__hashing = hashing


    def validate(
        self,
        user_id: UUID,
        new_password: str,
        old_password: str = None,
        current_password_check: bool = True
    ):
        user: User = self.__repository.get_one(
            key="user_id",
            value=user_id
        )

        if not user:
            raise NotFoundException()
        
        # check new and old password match
        is_current_password = self.__hashing.compare_password(
            password=new_password,
            hashed_password=user.password,
            throw_error=False
        )

        if is_current_password:
            raise IncorrectPassword()
        
        if current_password_check:
            if not old_password:
                raise ValueError("Old password required for check")
        
            self.__hashing.compare_password(
                password=old_password,
                hashed_password=user.password,
                detail="Incorrect password",
                throw_error=True
            )
            
        return True
        
        