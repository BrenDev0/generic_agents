from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from typing import List

from src.users.domain.entities import User
from src.persistence.infrastructure.sqlAlchemy.data_repository import SqlAlchemyDataRepository, Base

class SqlAlchemyUser(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    email_hash = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True, server_default=func.now())


class SqlAlchemyUsersRepository(SqlAlchemyDataRepository[User, SqlAlchemyUser]):
    def __init__(self):
        super().__init__(SqlAlchemyUser)
    
    def _to_entity(self, model: SqlAlchemyUser) -> User:
        return User(
            user_id=model.user_id,
            name=model.name,
            email=model.email,
            email_hash=model.email_hash,
            password=model.password,
            created_at=model.created_at,
            last_login=model.last_login
        )
    
    def _to_model(self, entity: User) -> SqlAlchemyUser:
        data = entity.model_dump(exclude={'user_id', 'created_at'} if not entity.user_id else set())
        return SqlAlchemyUser(**data)