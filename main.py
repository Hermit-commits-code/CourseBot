from ui.app import CourseApp
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = CourseApp(root)
    app.run()