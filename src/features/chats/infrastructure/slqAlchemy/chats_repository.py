from sqlalchemy import Column, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from typing import Optional
from src.persistence import Base, SqlAlchemyDataRepository
from src.features.agents import SqlAlchemyAgent, Agent
from ...domain import Chat


class SqlAlchemyChat(Base):
    __tablename__ = "chats"

    chat_id=Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    agent_id=Column(UUID(as_uuid=True), ForeignKey("agents.agent_id", ondelete="CASCADE"), nullable=False)
    created_at=Column(DateTime(timezone=True), nullable=True, server_default=func.now())

    agent = relationship("SqlAlchemyAgent")

class SqlAlchemyChatsRepository(SqlAlchemyDataRepository[Chat, SqlAlchemyChat]):
    def __init__(self):
        super().__init__(SqlAlchemyChat)

    def _to_entity(self, model: SqlAlchemyChat):
        return Chat(
            chat_id=model.chat_id,
            agent_id=model.agent_id,
            created_at=model.created_at,
            agent=self._agent_to_entity(model.agent)
        )
    
    def _agent_to_entity(self, agent_model: SqlAlchemyAgent) -> Optional[Agent]:
        if not agent_model:
            return None

        return Agent(
            agent_id=agent_model.agent_id,
            user_id=agent_model.user_id,
            name=agent_model.name,
            description=agent_model.description,
            created_at=agent_model.created_at
        )
    
    def _to_model(self, entity: Chat):
        data = entity.model_dump(exclude={"created_at", "agent"} if not entity.created_at else {"agent"})
        return SqlAlchemyChat(**data)