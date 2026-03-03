from langchain_community.utilities.sql_database import SQLDatabase
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from app.config_db import get_setting

def validate_db_connection(db_url: str) -> bool:
    """Validates if a connection can be established to the database URL."""
    try:
        engine = create_engine(db_url)
        with engine.connect() as conn:
            pass
        return True
    except SQLAlchemyError:
        return False

def get_configured_db_url() -> str | None:
    return get_setting("target_db_url")

def get_db(db_url: str) -> SQLDatabase:
    """Instantiates and returns a LangChain SQLDatabase from a SQLAlchemy connection string."""
    return SQLDatabase.from_uri(db_url)
