import tkinter as tk
from tkinter import simpledialog, messagebox
from data.database import Database

class CourseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Course Tracker")
        self.db = Database()

        # Main frame
        self.frame = tk.Frame(self.root, padx=10, pady=10)
        self.frame.pack()

        # Course list
        self.course_list = tk.Listbox(self.frame, width=50, height=20)
        self.course_list.pack()

        # Buttons frame
        self.button_frame = tk.Frame(self.frame)
        self.button_frame.pack(pady=5)

        # Add course button
        self.add_button = tk.Button(self.button_frame, text="Add Course", command=self.add_course_dialog)
        self.add_button.pack(side=tk.LEFT, padx=5)

        # Edit course button
        self.edit_button = tk.Button(self.button_frame, text="Edit Course", command=self.edit_course_dialog)
        self.edit_button.pack(side=tk.LEFT, padx=5)

        # Delete course button
        self.delete_button = tk.Button(self.button_frame, text="Delete Course", command=self.delete_course)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        # Reload button
        self.reload_button = tk.Button(self.button_frame, text="Reload", command=self.reload_app)
        self.reload_button.pack(side=tk.LEFT, padx=5)

        self.load_courses()

    def load_courses(self):
        self.course_list.delete(0, tk.END)
        courses = self.db.get_all_courses()
        for course in courses:
            self.course_list.insert(tk.END, f"{course[1]} - {course[2]} ({course[3]}, {course[4]}%)")

    def add_course_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Course")
        dialog.geometry("300x150")
        dialog.grab_set()

        tk.Label(dialog, text="Course Title:").pack(pady=5)
        title_entry = tk.Entry(dialog, width=30)
        title_entry.pack()

        tk.Label(dialog, text="Platform:").pack(pady=5)
        platform_entry = tk.Entry(dialog, width=30)
        platform_entry.pack()

        def submit():
            title = title_entry.get().strip()
            platform = platform_entry.get().strip()
            if title and platform:
                self.db.add_course(title, platform)
                self.load_courses()
                dialog.destroy()
                messagebox.showinfo("Success", f"Added '{title}' from {platform}")
            else:
                messagebox.showwarning("Input Error", "Please fill in both fields")

        tk.Button(dialog, text="Submit", command=submit).pack(pady=10)

    def edit_course_dialog(self):
        selected = self.course_list.curselection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a course to edit")
            return

        # Get course ID from selected item (assumes ID is first in tuple)
        course_str = self.course_list.get(selected[0])
        course_id = int(self.db.get_all_courses()[selected[0]][0])

        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Course")
        dialog.geometry("300x150")
        dialog.grab_set()

        tk.Label(dialog, text="Course Title:").pack(pady=5)
        title_entry = tk.Entry(dialog, width=30)
        title_entry.pack()
        title_entry.insert(0, self.db.get_all_courses()[selected[0]][1])  # Pre-fill title

        tk.Label(dialog, text="Platform:").pack(pady=5)
        platform_entry = tk.Entry(dialog, width=30)
        platform_entry.pack()
        platform_entry.insert(0, self.db.get_all_courses()[selected[0]][2])  # Pre-fill platform

        def submit():
            title = title_entry.get().strip()
            platform = platform_entry.get().strip()
            if title and platform:
                self.db.update_course(course_id, title=title, platform=platform)
                self.load_courses()
                dialog.destroy()
                messagebox.showinfo("Success", f"Updated course ID {course_id}")
            else:
                messagebox.showwarning("Input Error", "Please fill in both fields")

        tk.Button(dialog, text="Submit", command=submit).pack(pady=10)

    def delete_course(self):
        selected = self.course_list.curselection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a course to delete")
            return

        course_id = int(self.db.get_all_courses()[selected[0]][0])
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this course?"):
            self.db.delete_course(course_id)
            self.load_courses()
            messagebox.showinfo("Success", f"Deleted course ID {course_id}")

    def reload_app(self):
        self.db.close()
        self.db = Database()
        self.load_courses()
        messagebox.showinfo("Reload", "App reloaded successfully")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = CourseApp(root)
    app.run()