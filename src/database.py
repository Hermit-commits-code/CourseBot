import sqlite3

# Initialize the database
def init_db():
    conn = sqlite3.connect("course_tracker.db")
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    # Create courses table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        platform TEXT,
        progress INTEGER DEFAULT 0,
        start_date TEXT,
        completion_date TEXT,
        notes TEXT
    )
    """)

    conn.commit()
    conn.close()

# Add a new user
def add_user(username, password):
    conn = sqlite3.connect("course_tracker.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

# Authenticate a user
def authenticate_user(username, password):
    conn = sqlite3.connect("course_tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None

def add_course(name, platform, progress, start_date, completion_date, notes):
    """Insert a new course into the database."""
    conn = sqlite3.connect("course_tracker.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO courses (name, platform, progress, start_date, completion_date, notes)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, platform, progress, start_date, completion_date, notes))
    conn.commit()
    conn.close()