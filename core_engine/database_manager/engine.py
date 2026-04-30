"""
FraudShield - Database Engine
SQLite3 engine with WAL mode for concurrent read/write support.
"""

from sqlalchemy import create_engine, event
from core_engine.config.settings import settings


def _set_wal_mode(dbapi_conn, connection_record):
    """Enable WAL mode on every new SQLite connection for concurrent access."""
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def create_db_engine(database_url: str = None):
    """
    Create and return a SQLAlchemy engine configured for SQLite3 with WAL mode.

    Args:
        database_url: Optional override for database URL. Defaults to settings.

    Returns:
        SQLAlchemy Engine instance.
    """
    url = database_url or settings.DATABASE_URL
    engine = create_engine(
        url,
        echo=settings.DEBUG,
        pool_pre_ping=True,
        connect_args={"check_same_thread": False},
    )
    event.listen(engine, "connect", _set_wal_mode)
    return engine
