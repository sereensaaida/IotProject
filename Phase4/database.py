import sqlite3
cursor = None
conn = None

def initialize_cursor():
    DATABASE_FILE = "users.db"

    global conn
    # Connect to SQLite database
    conn = sqlite3.connect(DATABASE_FILE)
    global cursor
    cursor = conn.cursor()

def select_user(rfid):
    global cursor
    cursor.execute('''
    SELECT * FROM users WHERE rfid = :rfid
    ''', {'rfid': rfid})
    return cursor.fetchone()

def initialize_db():
    global conn
    global cursor
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
        ('33 08 d5 24', 'jayda grenada', 25.0, 70.0),  
        ('a3 2e db 04', 'manas mango', 20.0, 80.0)   
    ]
    cursor.executemany(
        'INSERT OR IGNORE INTO users (rfid, username, temp, light) VALUES (?, ?, ?, ?)', 
        users
    )
    
    # Commit changes
    conn.commit()
    print("Database initialized and populated successfully!")