from sqlalchemy import Column, ForeignKey, String, DateTime, func
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from src.shared.infrastructure.sqlAlchemy.data_repository import SqlAlchemyDataRepository, Base
from src.agents.domain.entities import Agent

class SqlAlchemyAgent(Base):
    __tablename__ ="agents"
    agent_id=Column(UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False)
    user_id=Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    name=Column(String, nullable=False)
    description=Column(String, nullable=True)
    created_at=Column(DateTime(timezone=True), nullable=True, server_default=func.now())


class SqlAlchemyAgentsRepository(SqlAlchemyDataRepository[Agent, SqlAlchemyAgent]):
    def __init__(self):
        super().__init__(SqlAlchemyAgent)

    def _to_entity(self, model: SqlAlchemyAgent) -> Agent:
        return  Agent(
            agent_id=model.agent_id,
            user_id=model.user_id,
            name=model.name,
            description=model.description,
            created_at=model.created_at
        )
    
    def _to_model(self, entity: Agent):
        data = entity.model_dump(exclude={"agent_id", "created_at"} if not entity.agent_id else set())
        return SqlAlchemyAgent(**data)
    
