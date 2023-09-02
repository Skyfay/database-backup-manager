import sqlite3
import os
def add_database():
    # The path to the SQLite Database.
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'local.db')
    # Create the database if it doesn't exist.
    conn = sqlite3.connect(db_path)
    conn.close()

def create_auth_table():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'local.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS auth (
                      id INTEGER PRIMARY KEY,
                      username TEXT UNIQUE NOT NULL,
                      password TEXT NOT NULL
                   )''')

    # Check if the table is empty.
    cursor.execute('SELECT COUNT(*) FROM auth')
    count = cursor.fetchone()[0]

    # If the table is empty, add the default admin user.
    if count == 0:
        cursor.execute('INSERT INTO auth (username, password) VALUES (?, ?)', ('Admin', 'Password'))
        conn.commit()

    conn.close()

