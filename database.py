import sqlite3
import os

DB_FILE = 'starcraft_matches.db'

def init_db():
    print("Initializing database...")
    conn = None
    try:
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
        print("matches table checked/created")
        
        c.execute('''
            CREATE TABLE IF NOT EXISTS user_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                replay_path TEXT
            )
        ''')
        print("user_info table checked/created")
        
        conn.commit()
        print("Database initialized and tables created/checked")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

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

def save_user_info(username, replay_path):
    conn = get_connection()
    if conn:
        try:
            c = conn.cursor()
            c.execute('INSERT OR REPLACE INTO user_info (id, username, replay_path) VALUES (1, ?, ?)', (username, replay_path))
            conn.commit()
            print("User info saved successfully")
        except sqlite3.Error as e:
            print(f"Error saving user info to database: {e}")
        finally:
            conn.close()

def get_user_info():
    conn = get_connection()
    if conn:
        try:
            c = conn.cursor()
            c.execute('SELECT username, replay_path FROM user_info WHERE id = 1')
            result = c.fetchone()
            return result if result else (None, None)
        except sqlite3.Error as e:
            print(f"Error retrieving user info from database: {e}")
            return None, None
        finally:
            conn.close()