import os
import sys

# Ensure the root directory is in the path so we can import 'core' and 'api'
sys.path.append(os.getcwd())

from core.database import create_db_engine, init_session_factory, create_all_tables, seed_rule_configs, get_db_session
from api.core_client import core_client

def seed():
    # Set default DB if not set
    if "DATABASE_URL" not in os.environ:
        os.environ["DATABASE_URL"] = "sqlite:///fraudshield.db"
        
    # 1. Initialize DB Structure
    print(f"Initializing database at {os.environ['DATABASE_URL']}...")
    engine = create_db_engine()
    init_session_factory(engine)
    create_all_tables(engine)
    
    with get_db_session() as session:
        seed_rule_configs(session)
    
    # 2. Generate and Score 1,000 Transactions (National Scale)
    print("Generating 1,000 synthetic transactions spanning 50 Indian cities...")
    try:
        created, flagged = core_client.generate_and_score(1000)
        print(f"Success! Created {created} transactions.")
        print(f"Risk Detection: {flagged} transactions flagged (MEDIUM/HIGH risk).")
        print("Phase 2: Data Initialization complete.")
    except Exception as e:
        print(f"Error during seeding: {str(e)}")

if __name__ == "__main__":
    seed()
