import os
os.environ["DATABASE_URL"] = "sqlite:///test_fraudshield.db"
from core.database import create_db_engine, init_session_factory, create_all_tables, seed_rule_configs, get_db_session

engine = create_db_engine()
init_session_factory(engine)
create_all_tables(engine)

# This physically creates the .db, .db-shm, and .db.wal files by connecting in WAL mode
with get_db_session() as session:
    seed_rule_configs(session)

print("Database files generated successfully.")
