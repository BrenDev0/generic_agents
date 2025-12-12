from typing import Dict, Any, Union
from src.users.domain.schemas import UpdateUser, VerifiedUserUpdate
from src.security.domain.services.encryption_service import EncryptionService
from src.security.domain.services.hashing_service import HashingService

class UpdateUser:
    def __init__(
        self, 
        encryption: EncryptionService,
        hashing: HashingService
    ):
        self.__encryption = encryption
        self.__hashing = hashing

    def execute(self, changes: Union[UpdateUser, VerifiedUserUpdate]) -> Dict[str, Any]:
        pass