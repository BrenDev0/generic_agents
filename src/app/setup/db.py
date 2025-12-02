import os
from sqlalchemy import create_engine, Engine

def get_engine() -> Engine:
    DB_URL = os.getenv("DATABASE_URL")
    engine = create_engine(DB_URL, pool_pre_ping=True)  

    return engine