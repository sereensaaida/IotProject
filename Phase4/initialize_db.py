import sqlite3

# Define the database file
DATABASE_FILE = 'users.db'

# Connect to SQLite database
conn = sqlite3.connect(DATABASE_FILE)
cursor = conn.cursor()

# Create the table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rfid_tag TEXT UNIQUE NOT NULL,
    temp_threshold REAL NOT NULL,
    light_threshold REAL NOT NULL
)
''')

# Insert data
users = [
    ('33 08 D5 24', 25.0, 70.0),  # User 1
    ('A3 2E D8 04', 30.0, 80.0)   # User 2
]
cursor.executemany('INSERT OR IGNORE INTO users (rfid_tag, temp_threshold, light_threshold) VALUES (?, ?, ?)', users)

# Commit and close
conn.commit()
conn.close()

print("Database initialized and populated successfully!")