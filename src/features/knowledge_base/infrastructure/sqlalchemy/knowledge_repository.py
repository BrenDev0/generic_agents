from sqlalchemy import Column, String, DateTime, func, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from src.persistence.infrastructure.sqlAlchemy.data_repository import SqlAlchemyDataRepository, Base
from src.features.knowledge_base.domain.entities import Knowledge

class SqlAlchemyKnowledge(Base):
    __tablename__ = "knowledge"

    knowledge_id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.agent_id", ondelete="CASCADE"), nullable=False)
    type = Column(String, nullable=False)
    name = Column(String, nullable=True)
    description = Column(String,  nullable=False)
    url = Column(String, nullable=True)
    is_embedded = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

class SqlAlchemyKnowledgeRepository(SqlAlchemyDataRepository[Knowledge, SqlAlchemyKnowledge]):
    def __init__(self):
        super().__init__(SqlAlchemyKnowledge)

    def _to_entity(self, model: SqlAlchemyKnowledge):
        return Knowledge(
            knowledge_id=model.knowledge_id,
            agent_id=model.agent_id,
            type=model.type,
            name=model.name,
            description=model.description,
            url=model.url,
            is_embedded=model.is_embedded,
            created_at=model.created_at
        )
    
    def _to_model(self, entity: Knowledge):
        data = entity.model_dump(exclude={"knowledge_id", "created_at"} if not entity.knowledge_id else set())
        return SqlAlchemyKnowledge(**data)