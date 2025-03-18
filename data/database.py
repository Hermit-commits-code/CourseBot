import sqlite3
import csv

class Database:
    def __init__(self, db_path="courses.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.ensure_user_id_column()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_settings (
                user_id INTEGER PRIMARY KEY,
                theme TEXT DEFAULT 'light',
                notifications_enabled BOOLEAN DEFAULT 1,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                title TEXT NOT NULL,
                platform TEXT,
                status TEXT DEFAULT 'Not Started',
                progress INTEGER DEFAULT 0,
                notes TEXT DEFAULT '',
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                course_id INTEGER,
                reminder_date TEXT NOT NULL,
                message TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id),
                FOREIGN KEY(course_id) REFERENCES courses(id)
            )
        ''')
        self.conn.commit()

    def ensure_user_id_column(self):
        # Check if the user_id column exists
        self.cursor.execute("PRAGMA table_info(courses)")
        columns = [info[1] for info in self.cursor.fetchall()]
        if 'user_id' not in columns:
            # Add the user_id column to the courses table
            self.cursor.execute("ALTER TABLE courses ADD COLUMN user_id INTEGER")
            self.conn.commit()

    # User-related methods
    def add_user(self, username, password):
        try:
            self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            self.conn.commit()
        except sqlite3.Error as e:
            raise ValueError(f"Failed to add user: {e}")

    def get_user(self, username, password):
        try:
            self.cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            raise ValueError(f"Failed to get user: {e}")

    def add_user_settings(self, user_id):
        try:
            self.cursor.execute("INSERT INTO user_settings (user_id) VALUES (?)", (user_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            raise ValueError(f"Failed to add user settings: {e}")

    def get_user_settings(self, user_id):
        try:
            self.cursor.execute("SELECT * FROM user_settings WHERE user_id = ?", (user_id,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            raise ValueError(f"Failed to get user settings: {e}")

    # Course-related methods (updated to include user_id)
    def add_course(self, user_id, title, platform, notes=""):
        try:
            self.cursor.execute("INSERT INTO courses (user_id, title, platform, notes) VALUES (?, ?, ?, ?)", (user_id, title, platform, notes))
            self.conn.commit()
        except sqlite3.Error as e:
            raise ValueError(f"Failed to add course: {e}")

    def get_all_courses(self, user_id):
        try:
            self.cursor.execute("SELECT * FROM courses WHERE user_id = ?", (user_id,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            raise ValueError(f"Failed to retrieve courses: {e}")

    def get_course_by_id(self, course_id):
        try:
            self.cursor.execute("SELECT * FROM courses WHERE id = ?", (course_id,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            raise ValueError(f"Failed to get course {course_id}: {e}")

    def update_course(self, course_id, title=None, platform=None, status=None, progress=None, notes=None):
        updates = []
        params = []
        if title is not None:
            updates.append("title = ?")
            params.append(title)
        if platform is not None:
            updates.append("platform = ?")
            params.append(platform)
        if status is not None:
            updates.append("status = ?")
            params.append(status)
        if progress is not None:
            updates.append("progress = ?")
            params.append(progress)
        if notes is not None:
            updates.append("notes = ?")
            params.append(notes)
        if updates:
            try:
                params.append(course_id)
                query = f"UPDATE courses SET {', '.join(updates)} WHERE id = ?"
                self.cursor.execute(query, params)
                self.conn.commit()
            except sqlite3.Error as e:
                raise ValueError(f"Failed to update course {course_id}: {e}")

    def delete_course(self, course_id):
        try:
            self.cursor.execute("DELETE FROM courses WHERE id = ?", (course_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            raise ValueError(f"Failed to delete course {course_id}: {e}")

    def export_to_csv(self, user_id, filename="courses.csv"):
        try:
            courses = self.get_all_courses(user_id)
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["id", "user_id", "title", "platform", "status", "progress", "notes"])
                for course in courses:
                    writer.writerow(course)
            return True
        except (sqlite3.Error, IOError) as e:
            raise ValueError(f"Failed to export to {filename}: {e}")

    def import_from_csv(self, user_id, filename="courses.csv"):
        count = 0
        try:
            with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                header = next(reader)  # Skip header
                for row in reader:
                    if len(row) == 6:
                        row.insert(1, user_id)  # Add user_id if missing
                    if len(row) == 7:
                        id, user_id, title, platform, status, progress, notes = row
                        if not title or not platform:
                            continue  # Skip invalid rows
                        self.cursor.execute(
                            "INSERT INTO courses (user_id, title, platform, status, progress, notes) VALUES (?, ?, ?, ?, ?, ?)",
                            (user_id, title, platform, status, progress, notes)
                        )
                        count += 1
                self.conn.commit()
            print(f"Imported {count} courses from {filename}")
            return count
        except FileNotFoundError:
            return 0
        except Exception as e:
            raise ValueError(f"Failed to import from {filename}: {e}")

    # Reminder-related methods
    def add_reminder(self, user_id, course_id, reminder_date, message=""):
        try:
            self.cursor.execute("INSERT INTO reminders (user_id, course_id, reminder_date, message) VALUES (?, ?, ?, ?)",
                                (user_id, course_id, reminder_date, message))
            self.conn.commit()
        except sqlite3.Error as e:
            raise ValueError(f"Failed to add reminder: {e}")

    def get_reminders(self, user_id):
        try:
            self.cursor.execute("SELECT * FROM reminders WHERE user_id = ?", (user_id,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            raise ValueError(f"Failed to retrieve reminders: {e}")

    def delete_reminder(self, reminder_id):
        try:
            self.cursor.execute("DELETE FROM reminders WHERE id = ?", (reminder_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            raise ValueError(f"Failed to delete reminder {reminder_id}: {e}")

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    db = Database("courses.db")
    db.add_course(1, "Test Course", "Udemy", "Great intro")
    print(db.get_course_by_id(1))
    db.close()