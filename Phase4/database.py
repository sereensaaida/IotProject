import sqlite3

DB_FILE = "users.db"

def insert_or_update_temperature_and_light(rfid_tag, temp_threshold, light_threshold):
    """
    Insert or update the temperature and light intensity for a specific user based on their RFID tag.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Check if the user exists by RFID tag
    cursor.execute('''
    SELECT * FROM users WHERE rfid_tag = ?
    ''', (rfid_tag,))
    
    user = cursor.fetchone()

    if user:
        # If user exists, update the temperature and light intensity
        cursor.execute('''
        UPDATE users
        SET temp_threshold = ?, light_threshold = ?
        WHERE rfid_tag = ?
        ''', (temp_threshold, light_threshold, rfid_tag))
    else:
        # If user does not exist, insert the new data
        cursor.execute('''
        INSERT INTO users (rfid_tag, temp_threshold, light_threshold)
        VALUES (?, ?, ?)
        ''', (rfid_tag, temp_threshold, light_threshold))
    
    conn.commit()
    conn.close()
    print(f"Updated/Inserted RFID: {rfid_tag} with temp: {temp_threshold} and light: {light_threshold}")
