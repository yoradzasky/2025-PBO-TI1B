# database.py
import sqlite3
import pandas as pd
from konfigurasi import DB_PATH  # Use path from konfigurasi

def get_db_connection() -> sqlite3.Connection | None:
    """Open and return a new connection to the SQLite database."""
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row  # Access columns by name
        return conn
    except sqlite3.Error as e:
        print(f"ERROR [database.py] Database connection failed: {e}")
        return None

def execute_query(query: str, params: tuple = None):
    """Execute a non-SELECT query. Returns lastrowid if INSERT."""
    conn = get_db_connection()
    if not conn:
        return None
    last_id = None
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        last_id = cursor.lastrowid
        return last_id
    except sqlite3.Error as e:
        print(f"ERROR [database.py] Query failed: {e} | Query: {query[:60]}")
        conn.rollback()
        return None
    finally:
        if conn:
            conn.close()

def fetch_query(query: str, params: tuple = None, fetch_all: bool = True):
    """Execute a SELECT query and return results."""
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        result = cursor.fetchall() if fetch_all else cursor.fetchone()
        return result
    except sqlite3.Error as e:
        print(f"ERROR [database.py] Fetch failed: {e} | Query: {query[:60]}")
        return None
    finally:
        if conn:
            conn.close()

def get_dataframe(query: str, params: tuple = None) -> pd.DataFrame:
    """Execute a SELECT query and return a Pandas DataFrame."""
    conn = get_db_connection()
    if not conn:
        return pd.DataFrame()
    try:
        df = pd.read_sql_query(query, conn, params=params)
        return df
    except Exception as e:
        print(f"ERROR [database.py] Failed to read to DataFrame: {e}")
        return pd.DataFrame()
    finally:
        if conn:
            conn.close()

def save_user_profile(profile: dict):
    """Insert or update the single user profile (always id=1)."""
    sql = """
    INSERT INTO user_profile (id, name, age, height, gender, weight, daily_target)
    VALUES (1, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(id) DO UPDATE SET
        name=excluded.name,
        age=excluded.age,
        height=excluded.height,
        gender=excluded.gender,
        weight=excluded.weight,
        daily_target=excluded.daily_target;
    """
    params = (
        profile['name'], profile['age'], profile['height'],
        profile['gender'], profile['weight'], profile['daily_target']
    )
    return execute_query(sql, params)

def load_user_profile():
    """Get user profile as dict (returns default if none)."""
    row = fetch_query("SELECT * FROM user_profile WHERE id = 1", fetch_all=False)
    if row:
        return dict(row)
    return {
        'name': '',
        'age': 25,
        'height': 170,
        'gender': 'Male',
        'weight': 70.0,
        'daily_target': 2000
    }


def setup_database_initial():
    """Ensure the tables for nutrition entries, user weights, and user profile exist."""
    print(f"Checking/creating tables in database (via database.py): {DB_PATH}")
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()

        # Create user profile table
        sql_create_profile_table = """
        CREATE TABLE IF NOT EXISTS user_profile (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            name TEXT,
            age INTEGER,
            height INTEGER,
            gender TEXT,
            weight REAL,
            daily_target INTEGER
        );
        """
        cursor.execute(sql_create_profile_table)

        # Create nutrition table
        sql_create_nutrition_table = """
        CREATE TABLE IF NOT EXISTS nutrition_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            deskripsi TEXT NOT NULL,
            jumlah REAL NOT NULL CHECK(jumlah > 0),
            kategori TEXT,
            tanggal DATE NOT NULL
        );
        """
        # Create weight table
        sql_create_weight_table = """
        CREATE TABLE IF NOT EXISTS user_weights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            weight REAL NOT NULL CHECK(weight > 0),
            tanggal DATE NOT NULL
        );
        """

        cursor.execute(sql_create_nutrition_table)
        cursor.execute(sql_create_weight_table)
        conn.commit()
        print(" -> Tables 'user_profile', 'nutrition_entries', and 'user_weights' are ready.")
        return True
    except sqlite3.Error as e:
        print(f"Error SQLite during table setup: {e}")
        return False
    finally:
        if conn:
            conn.close()
