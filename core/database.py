"""FraudShield - Database Management"""
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from core import settings
from core.models import Base, RuleConfigModel

_SessionFactory = None

def _set_wal_mode(dbapi_conn, connection_record):
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

def create_db_engine(database_url: str = None):
    url = database_url or settings.DATABASE_URL
    engine = create_engine(url, echo=settings.DEBUG, pool_pre_ping=True, connect_args={"check_same_thread": False})
    event.listen(engine, "connect", _set_wal_mode)
    return engine

def init_session_factory(engine):
    global _SessionFactory
    factory = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    _SessionFactory = scoped_session(factory)
    return _SessionFactory

def get_session_factory():
    if _SessionFactory is None:
        raise RuntimeError("Session factory not initialized.")
    return _SessionFactory

@contextmanager
def get_db_session():
    factory = get_session_factory()
    session: Session = factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def create_all_tables(engine):
    Base.metadata.create_all(bind=engine)

def seed_rule_configs(session):
    if session.query(RuleConfigModel).count() > 0:
        return 0
    configs = []
    for rule_name, params in settings.DEFAULT_RULE_WEIGHTS.items():
        configs.append(RuleConfigModel(
            id=str(uuid.uuid4()), rule_name=rule_name, weight=params["weight"],
            threshold=params["threshold"], is_active=True, updated_at=datetime.now(timezone.utc)
        ))
    for c in configs: session.add(c)
    session.flush()
    return len(configs)
