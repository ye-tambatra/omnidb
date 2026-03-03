import sqlite3
import os

CONFIG_DB_PATH = os.getenv("CONFIG_DB_PATH", "omnidb_config.sqlite")

def get_config_db_connection():
    """Returns a connection to the SQLite configuration database."""
    conn = sqlite3.connect(CONFIG_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_config_db():
    """Initializes the configuration database with default permission levels."""
    conn = get_config_db_connection()
    cursor = conn.cursor()
    
    # Create the permissions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS permissions (
            level INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            allowed_operations TEXT NOT NULL
        )
    ''')
    
    # Create the settings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    ''')
    
    # Insert default permissions if the table is empty
    cursor.execute('SELECT COUNT(*) FROM permissions')
    if cursor.fetchone()[0] == 0:
        default_permissions = [
            (1, 'Read-Only', 'SELECT,SHOW,DESCRIBE,EXPLAIN'),
            (2, 'Data Entry', 'SELECT,SHOW,DESCRIBE,EXPLAIN,INSERT'),
            (3, 'Full Admin', 'SELECT,SHOW,DESCRIBE,EXPLAIN,INSERT,UPDATE,DELETE,ALTER,DROP,CREATE,TRUNCATE,REPLACE')
        ]
        cursor.executemany('''
            INSERT INTO permissions (level, name, allowed_operations)
            VALUES (?, ?, ?)
        ''', default_permissions)
        conn.commit()
    
    conn.close()

def get_allowed_operations(level: int) -> list[str]:
    """Retrieves the list of allowed SQL operations for a given permission level."""
    conn = get_config_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT allowed_operations FROM permissions WHERE level = ?', (level,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return [op.strip().upper() for op in row['allowed_operations'].split(',')]
    return []

def update_allowed_operations(level: int, allowed_operations: str):
    """Updates the allowed operations for a specific level."""
    conn = get_config_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE permissions
        SET allowed_operations = ?
        WHERE level = ?
    ''', (allowed_operations.upper(), level))
    conn.commit()
    conn.close()

def get_all_permissions():
    """Returns all configured permissions."""
    conn = get_config_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM permissions')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_setting(key: str) -> str | None:
    """Retrieves a configuration value from the settings table."""
    conn = get_config_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
    row = cursor.fetchone()
    conn.close()
    return row['value'] if row else None

def set_setting(key: str, value: str):
    """Sets a configuration value in the settings table."""
    conn = get_config_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO settings (key, value) VALUES (?, ?)
        ON CONFLICT(key) DO UPDATE SET value = excluded.value
    ''', (key, value))
    conn.commit()
    conn.close()
