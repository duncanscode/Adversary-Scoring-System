import sqlite3
import os

DB_FILE = 'starcraft_matches.db'

def init_db():
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS matches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                opponent_name TEXT,
                map_name TEXT,
                wins INTEGER,
                losses INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
        print("Database initialized and table created")

def get_connection():
    """Create a database connection to the SQLite database."""
    try:
        conn = sqlite3.connect(DB_FILE)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def fetch_data(query, params=()):
    """Fetch data from the database using the provided query and parameters."""
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(query, params)
            rows = cur.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            return None
        finally:
            conn.close()

def save_to_db(opponent_name, map_name, wins, losses):
    conn = get_connection()
    if conn:
        try:
            c = conn.cursor()
            c.execute('''
                INSERT INTO matches (opponent_name, map_name, wins, losses)
                VALUES (?, ?, ?, ?)
            ''', (opponent_name, map_name, wins, losses))
            conn.commit()
            print("Data saved successfully")
        except sqlite3.Error as e:
            print(f"Error saving to database: {e}")
        finally:
            conn.close()

# Initialize the database when this module is imported
init_db()