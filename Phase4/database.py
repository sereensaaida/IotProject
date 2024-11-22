import sqlite3

DATABASE_FILE = "users.db"

# Connect to SQLite database
conn = sqlite3.connect(DATABASE_FILE)
cursor = conn.cursor()

def select_user(rfid):
    cursor.execute('''
    SELECT * FROM users WHERE rfid = :rfid
    ''', {'rfid': rfid})
    return cursor.fetchall()

def initialize_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        rfid TEXT UNIQUE NOT NULL,
        username TEXT NOT NULL,
        temp REAL NOT NULL,
        light REAL NOT NULL
    )
    ''')

    # Insert data
    users = [
        ('33 08 D5 24', 'jayda grenada', 25.0, 70.0),  
        ('A3 2E D8 04', 'manas mango', 30.0, 80.0)   
    ]
    cursor.executemany(
        'INSERT OR IGNORE INTO users (rfid, username, temp, light) VALUES (?, ?, ?, ?)', 
        users
    )
    
    # Commit changes
    conn.commit()
    print("Database initialized and populated successfully!")