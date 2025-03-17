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
        try:
            self.cursor.execute("INSERT INTO courses (title, platform, notes) VALUES (?, ?, ?)", (title, platform, notes))
            self.conn.commit()
        except sqlite3.Error as e:
            raise ValueError(f"Failed to add course: {e}")

    def get_all_courses(self):
        try:
            self.cursor.execute("SELECT * FROM courses")
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

    def export_to_csv(self, filename="courses.csv"):
        try:
            courses = self.get_all_courses()
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["id", "title", "platform", "status", "progress", "notes"])
                for course in courses:
                    writer.writerow(course)
            return True
        except (sqlite3.Error, IOError) as e:
            raise ValueError(f"Failed to export to {filename}: {e}")

    def import_from_csv(self, filename="courses.csv"):
        count = 0
        try:
            with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                header = next(reader)  # Skip header
                if len(header) < 5:
                    raise ValueError("CSV file missing required columns")
                for row in reader:
                    row = row + [""] * (6 - len(row))  # Pad short rows
                    id, title, platform, status, progress, notes = row
                    if not title or not platform:
                        continue  # Skip invalid rows
                    try:
                        progress = int(progress or 0)
                        if not 0 <= progress <= 100:
                            progress = 0  # Reset invalid progress
                    except ValueError:
                        progress = 0
                    status = status if status in ["Not Started", "In Progress", "Completed"] else "Not Started"
                    self.cursor.execute(
                        "INSERT INTO courses (title, platform, status, progress, notes) VALUES (?, ?, ?, ?, ?)",
                        (title, platform, status, progress, notes)
                    )
                    count += 1
                self.conn.commit()
            print(f"Imported {count} courses from {filename}")
            return count
        except FileNotFoundError:
            return 0
        except Exception as e:
            raise ValueError(f"Failed to import from {filename}: {e}")

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    db = Database()
    db.add_course("Test Course", "Udemy", "Great intro")
    print(db.get_course_by_id(1))
    db.close()