from ...domain import CreateMessageRequest, MessageRepository
from ..service import MessageService

class CreateMessage:
    def __init__(
        self,
        message_repository: MessageRepository,
        message_service: MessageService
    ):
        self.__message_repository = message_repository
        self.__message_service = message_service

    def execute(
        self,
        data: CreateMessageRequest
    ):
        partial_entity = self.__message_service.prepare_new_message_data(
            data=data
        )

        new_message = self.__message_repository.create(data=partial_entity)

        return self.__message_service.get_decrypted_entity(new_message)
        

