from src.security import EncryptionService
from ..domain import Message, MessagePublic, CreateMessageRequest


class MessageService:
    def __init__(
        self,
        encryption: EncryptionService
    ):
        self.__encryption = encryption

    def prepare_new_message_data(
        self,
        data: CreateMessageRequest
    ) -> Message:
        encrypted_text = self.__encryption.encrypt(data.text)

        return Message(
            chat_id=data.chat_id,
            type=data.type,
            text=encrypted_text
        )
    
    def get_public_schema(
        self,
        entity: Message
    ) -> MessagePublic:
        return MessagePublic(
            message_id=entity.message_id,
            chat_id=entity.chat_id,
            type=entity.type,
            text=self.__encryption.decrypt(entity.text),
            created_at=entity.created_at
        )
