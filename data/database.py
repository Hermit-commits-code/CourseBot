import sqlite3
import csv

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(":memory:")
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                platform TEXT,
                status TEXT DEFAULT 'Not Started',
                progress INTEGER DEFAULT 0,
                notes TEXT DEFAULT ''
            )
        ''')
        self.conn.commit()

    def add_course(self, title, platform, notes=""):
        self.cursor.execute("INSERT INTO courses (title, platform, notes) VALUES (?, ?, ?)", (title, platform, notes))
        self.conn.commit()

    def get_all_courses(self):
        self.cursor.execute("SELECT * FROM courses")
        return self.cursor.fetchall()

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
            params.append(course_id)
            query = f"UPDATE courses SET {', '.join(updates)} WHERE id = ?"
            self.cursor.execute(query, params)
            self.conn.commit()

    def delete_course(self, course_id):
        self.cursor.execute("DELETE FROM courses WHERE id = ?", (course_id,))
        self.conn.commit()

    def export_to_csv(self, filename="courses.csv"):
        courses = self.get_all_courses()
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # Write header
            writer.writerow(["id", "title", "platform", "status", "progress", "notes"])
            # Write data
            for course in courses:
                writer.writerow(course)

    def import_from_csv(self, filename="courses.csv"):
        try:
            with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip header
                for row in reader:
                    # Ensure row has enough columns, fill missing with defaults
                    row = row + [""] * (6 - len(row))
                    id, title, platform, status, progress, notes = row
                    # Insert without ID (let SQLite assign new IDs)
                    self.cursor.execute(
                        "INSERT INTO courses (title, platform, status, progress, notes) VALUES (?, ?, ?, ?, ?)",
                        (title, platform, status or "Not Started", int(progress or 0), notes)
                    )
                self.conn.commit()
        except FileNotFoundError:
            pass  # Silently ignore if file doesn't exist (fresh start)
        except Exception as e:
            print(f"Error importing CSV: {e}")

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    db = Database()
    db.add_course("Test Course", "Udemy", "Great intro")
    db.export_to_csv()
    db.close()