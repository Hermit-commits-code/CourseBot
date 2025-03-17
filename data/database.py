import sqlite3

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
                progress INTEGER DEFAULT 0
            )
        ''')
        self.conn.commit()

    def add_course(self, title, platform):
        self.cursor.execute("INSERT INTO courses (title, platform) VALUES (?, ?)", (title, platform))
        self.conn.commit()

    def get_all_courses(self):
        self.cursor.execute("SELECT * FROM courses")
        return self.cursor.fetchall()

    def update_course(self, course_id, title=None, platform=None, status=None, progress=None):
        # Only update fields that are provided
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
        if updates:
            params.append(course_id)
            query = f"UPDATE courses SET {', '.join(updates)} WHERE id = ?"
            self.cursor.execute(query, params)
            self.conn.commit()

    def delete_course(self, course_id):
        self.cursor.execute("DELETE FROM courses WHERE id = ?", (course_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    db = Database()
    db.add_course("Test Course", "Udemy")
    print(db.get_all_courses())
    db.update_course(1, title="Updated Course")
    print(db.get_all_courses())
    db.delete_course(1)
    print(db.get_all_courses())
    db.close()