from src.persistence import DataRepository

class GetMessageCollection:
    def __init__(
        self,
        message_repository: DataRepository
    ):
        self.__