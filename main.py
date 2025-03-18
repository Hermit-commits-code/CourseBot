from desktop.ui.app import CourseApp
from desktop.data.database import Database
import tkinter as tk

if __name__ == "__main__":
    db = Database("courses.db")
    root = tk.Tk()
    app = CourseApp(root, db)
    app.run()
    db.close()