from abc import ABC, abstractmethod
from src.persistence import DataRepository
from typing import List, Union
from uuid import UUID
from .entities import Message

class MessageRepository(DataRepository, ABC):
    @abstractmethod
    def delete_many(self, key: str, value: List[Union[str, UUID, int]]) -> List[Message]:
        raise NotImplementedError