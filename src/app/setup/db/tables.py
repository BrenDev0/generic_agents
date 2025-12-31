import logging
from src.app.setup.db.engine import get_engine
from src.users.infrastructure.sqlAlchemy.users_repository import SqlAlchemyUser
from src.agents.infrastructure.sqlAlchemy.agents_repository import SqlAlchemyAgent
from src.agent_settings.infrastructure.sqlAlechemy.agent_settings_repository import SqlAlchemyAgentSettings
from src.persistence.infrastructure.sqlAlchemy.data_repository import Base
logger = logging.getLogger(__name__)

def create_tables():
    try:
        engine = get_engine()
        Base.metadata.create_all(bind=engine)
    
    except Exception as e:
        logger.error(str(e))