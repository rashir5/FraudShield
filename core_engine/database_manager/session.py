"""
FraudShield - Database Session Management
Scoped session factory with context manager support.
"""

from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker, scoped_session, Session


_SessionFactory = None


def init_session_factory(engine):
    """Initialize the global session factory with the given engine."""
    global _SessionFactory
    factory = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    _SessionFactory = scoped_session(factory)
    return _SessionFactory


def get_session_factory():
    """Return the current session factory. Must call init_session_factory first."""
    if _SessionFactory is None:
        raise RuntimeError("Session factory not initialized. Call init_session_factory(engine) first.")
    return _SessionFactory


@contextmanager
def get_db_session():
    """
    Context manager that yields a database session and handles
    commit/rollback/close automatically.

    Usage:
        with get_db_session() as session:
            session.query(...)
    """
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
