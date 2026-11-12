import sqlite3

conn = sqlite3.connect("database.db")

# USERS TABLE
conn.execute("""
CREATE TABLE users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
email TEXT,
password TEXT
)
""")

# HISTORY TABLE
conn.execute("""
CREATE TABLE history(
id INTEGER PRIMARY KEY AUTOINCREMENT,
user TEXT,
crop TEXT,
fertilizer TEXT,
date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("Database Ready ✔")