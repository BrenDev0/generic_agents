from sqlalchemy import Column, String, DateTime, func, ForeignKey, delete
from sqlalchemy.dialects.postgresql import UUID
import uuid
from typing import List, Union
from src.persistence import SqlAlchemyDataRepository, Base
from ...domain import Message, MessageRepository

class SqlAlchemyMessage(Base):
    __tablename__ = "Messages"

    message_id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, defualt=uuid.uuid4)
    chat_id = Column(UUID(as_uuid=True), ForeignKey("chats", ondelete="CASCADE"), nullable=False)
    type = Column(String, nullable=False)
    text = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())


class SqlAlchemyMessageRepository(SqlAlchemyDataRepository[Message, SqlAlchemyMessage], MessageRepository):
    def __init__(self):
        super().__init__(SqlAlchemyMessage)


    def delete_many(self, key: str, value: List[Union[str, uuid.UUID]]) -> List[Message]:
        stmt = delete(self.model).where(
            getattr(self.model, key).in_(value)
        ).returning(*self.model.__table__.c)

        with self._get_session() as db:
            result = db.execute(stmt)
            db.commit()
            
            deleted_rows = result.fetchall()
            
            if not deleted_rows:
                return []
        
            return [
                self._to_entity(self.model(**row._mapping)) 
                for row in deleted_rows
            ]

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

