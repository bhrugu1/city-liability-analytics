import sqlite3
import os

db_path = os.path.join('..', '..', 'data', 'processed', 'city_claims.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables in database:", tables)

if tables:
    # Check row count
    cursor.execute("SELECT COUNT(*) FROM claims;")
    count = cursor.fetchone()[0]
    print(f"Number of rows in claims table: {count}")
    
    # Check first few rows
    cursor.execute("SELECT * FROM claims LIMIT 3;")
    rows = cursor.fetchall()
    print("First 3 rows:")
    for row in rows:
        print(row)

conn.close()
