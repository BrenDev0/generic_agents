from sqlalchemy import Column, ForeignKey, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from ...domain import Chat
from src.persistence.infrastructure.sqlAlchemy.data_repository import Base, SqlAlchemyDataRepository

class SqlAlchemyChat(Base):
    __tablename__ = "chats"

    chat_id=Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    agent_id=Column(UUID(as_uuid=True), ForeignKey("agents.agent_id", ondelete="CASCADE"), nullable=False)
    created_at=Column(DateTime(timezone=True), nullable=True, server_default=func.now())


class SqlAlchemyChatsRepository(SqlAlchemyDataRepository[Chat, SqlAlchemyChat]):
    def __init__(self):
        super().__init__(SqlAlchemyChat)

    def _to_entity(self, model: SqlAlchemyChat):
        return Chat(
            chat_id=model.chat_id,
            agent_id=model.agent_id,
            created_at=model.created_at
        )
    
    def _to_model(self, entity: Chat):
        data = entity.model_dump(exclude={"chat_id"} if not entity.chat_id else set())
        return SqlAlchemyChat(**data)