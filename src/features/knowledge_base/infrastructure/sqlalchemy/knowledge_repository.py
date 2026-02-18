from sqlalchemy import Column, String, DateTime, func, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from typing import Optional
from sqlalchemy.orm import relationship
from uuid import uuid4
from src.persistence.infrastructure.sqlAlchemy.data_repository import SqlAlchemyDataRepository, Base
from src.features.agents import SqlAlchemyAgent, Agent
from ...domain import Knowledge

class SqlAlchemyKnowledge(Base):
    __tablename__ = "knowledge"

    knowledge_id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.agent_id", ondelete="CASCADE"), nullable=False)
    type = Column(String, nullable=False)
    size = Column(String, nullable=True)
    name = Column(String, nullable=True)
    description = Column(String,  nullable=False)
    url = Column(String, nullable=True)
    state = Column(String, nullable=False, default="NO PROCESADO")
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    
    agent = relationship("SqlAlchemyAgent")

class SqlAlchemyKnowledgeRepository(SqlAlchemyDataRepository[Knowledge, SqlAlchemyKnowledge]):
    def __init__(self):
        super().__init__(SqlAlchemyKnowledge)

    def _to_entity(self, model: SqlAlchemyKnowledge):
        return Knowledge(
            knowledge_id=model.knowledge_id,
            agent_id=model.agent_id,
            type=model.type,
            size=model.size,
            name=model.name,
            description=model.description,
            url=model.url,
            state=model.state,
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
    
    def _to_model(self, entity: Knowledge):
        data = entity.model_dump(exclude={"knowledge_id", "created_at", "agent"} if not entity.knowledge_id else {"agent"})
        return SqlAlchemyKnowledge(**data)