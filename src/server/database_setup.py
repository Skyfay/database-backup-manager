import sqlite3
import os
def add_database():
    # Der Pfad zur SQLite-Datenbankdatei
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'local.db')
    # Verbindung zur Datenbank herstellen oder erstellen, wenn sie nicht vorhanden ist
    conn = sqlite3.connect(db_path)
    print("INFO: Database created at or connected.")
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

    # Überprüfen, ob die Tabelle leer ist (keine Einträge)
    cursor.execute('SELECT COUNT(*) FROM auth')
    count = cursor.fetchone()[0]

    # Wenn die Tabelle leer ist, fügen Sie den Standardbenutzer 'Admin' hinzu
    if count == 0:
        cursor.execute('INSERT INTO auth (username, password) VALUES (?, ?)', ('Admin', 'Password'))
        conn.commit()

    conn.close()

