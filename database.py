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
        instructor TEXT,
        category TEXT,
        progress INTEGER DEFAULT 0,
        start_date TEXT,
        completion_date TEXT,
        course_url TEXT,
        course_notes TEXT,
        attachments TEXT,
        changelog TEXT
    )
    """)

    conn.commit()
    conn.close()
    print("Database initialized successfully!")

# Add a new user
def add_user(username, password):
    try:
        conn = sqlite3.connect("course_tracker.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        print(f"User '{username}' added successfully!")
    except sqlite3.IntegrityError:
        print(f"Error: User '{username}' already exists.")

# Authenticate a user
def authenticate_user(username, password):
    conn = sqlite3.connect("course_tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None

# Test the database setup
if __name__ == "__main__":
    init_db()
    # Add a test user (optional)
    add_user("testuser", "password123")
    # Test authentication
    if authenticate_user("testuser", "password123"):
        print("Authentication successful!")
    else:
        print("Authentication failed!")