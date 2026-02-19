from sqlalchemy import Column, String, DateTime, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from src.persistence import SqlAlchemyDataRepository, Base
from ...domain import Message

class SqlAlchemyMessage(Base):
    __tablename__ = "Messages"

    message_id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, defualt=uuid4)
    chat_id = Column(UUID(as_uuid=True), ForeignKey("chats", ondelete="CASCADE"), nullable=False)
    type = Column(String, nullable=False)
    text = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())


class SqlAlchemyMessageRepository(SqlAlchemyDataRepository[Message, SqlAlchemyMessage]):
    def __init__(self):
        super().__init__(SqlAlchemyMessage)

    def _to_entity(self, model):
        return Message(
            message_id=model.message_id,
            chat_id=model.chat_id,
            type=model.type,
            text=model.text,
            created_at=model.created_at
        )
    
    def _to_model(self, entity):
        data = entity.model_dump(exclude={"message_id", "created_at"} if not entity.message_id else set())

        return SqlAlchemyMessage(**data)

