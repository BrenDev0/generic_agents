from sqlalchemy import Column, ForeignKey, String, Float, Boolean
from uuid import uuid4
from typing import Optional
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.agent_settings.domain.entities import AgentSettings
from src.agents.domain.entities import Agent
from src.shared.infrastructure.sqlAlchemy.data_repository import Base, SqlAlchemyDataRepository
from src.agents.infrastructure.sqlAlchemy.agents_repository import SqlAlchemyAgent

class SqlAlchemyAgentSettings(Base):
    __tablename__ = "agent_settings"

    setting_id=Column(UUID(as_uuid=True), primary_key=True, defualt=uuid4, nullable=False)
    agent_id=Column(UUID(as_uuid=True), ForeignKey("agents.agent_id", ondelete="CASCADE"), nullable=False)
    system_prompt=Column(String, nullable=False)
    temperature=Column(Float, nullable=False)
    transcripts=Column(Boolean, nullable=False, default=False)
    
    agent = relationship(SqlAlchemyAgent)

class SqlAlchemyAgentSettingsRepository(SqlAlchemyDataRepository[AgentSettings, SqlAlchemyAgentSettings]):
    def __init__(self):
        super().__init__(SqlAlchemyAgentSettings)

    
    def _to_entity(self, model: SqlAlchemyAgentSettings) -> AgentSettings:
        return AgentSettings(
            setting_id=model.setting_id,
            agent_id=model.agent_id,
            system_prompt=model.system_prompt,
            temperature=model.temperature,
            transcripts=model.transcripts,
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
    
    def _to_model(self, entity: AgentSettings):
        data = entity.model_dump(exclude={"setting_id"} if not entity.agent_id else set())
        return SqlAlchemyAgentSettings(**data)