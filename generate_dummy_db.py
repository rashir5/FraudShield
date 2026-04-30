import sqlite3

# Connect to the DB (creates test_fraudshield.db)
conn = sqlite3.connect('test_fraudshield.db')
cursor = conn.cursor()

# Enable WAL mode (creates the .wal and .shm files)
cursor.execute('PRAGMA journal_mode=WAL;')

# Create the basic tables so the database is not empty
cursor.execute('''CREATE TABLE rule_config (id TEXT PRIMARY KEY, rule_name TEXT, weight REAL, threshold REAL, is_active INTEGER, updated_at TEXT)''')
cursor.execute("INSERT INTO rule_config (id, rule_name, weight, threshold, is_active) VALUES ('1', 'velocity', 0.3, 3.0, 1)")

conn.commit()
conn.close()

print("Test database files with WAL mode generated successfully.")
