import sqlite3

# Connect to your SQLite database
conn = sqlite3.connect("db.sqlite")
cursor = conn.cursor()

# See all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables:", tables)

# View data from a specific table (replace 'your_table_name')
cursor.execute("SELECT * FROM your_table_name")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
