import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
from tkinter import ttk
from data.database import Database

class CourseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Course Tracker")
        self.db = Database()
        self.db.import_from_csv()
        self.courses_cache = list(self.db.get_all_courses())  # Cache initial data

        self.style = ttk.Style()
        self.current_theme = "light"
        self.configure_theme()

        self.frame = tk.Frame(self.root, padx=10, pady=10)
        self.frame.pack(fill="both", expand=True)

        self.dashboard_frame = tk.Frame(self.frame, borderwidth=2, relief="groove")
        self.dashboard_frame.grid(row=0, column=0, columnspan=2, pady=5, sticky="ew")

        self.total_label = tk.Label(self.dashboard_frame, text="Total Courses: 0")
        self.total_label.pack(side=tk.LEFT, padx=5)

        self.completed_label = tk.Label(self.dashboard_frame, text="Completed: 0")
        self.completed_label.pack(side=tk.LEFT, padx=5)

        self.progress_label = tk.Label(self.dashboard_frame, text="Avg Progress: 0%")
        self.progress_label.pack(side=tk.LEFT, padx=5)

        self.search_frame = tk.Frame(self.frame)
        self.search_frame.grid(row=1, column=0, columnspan=2, pady=5, sticky="ew")

        tk.Label(self.search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_entry = tk.Entry(self.search_frame, width=40)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind("<KeyRelease>", self.filter_courses)

        self.tree = ttk.Treeview(self.frame, columns=("title", "platform", "status", "progress", "notes"), show="headings", height=20)
        self.tree.grid(row=2, column=0, sticky="nsew")

        self.tree.heading("title", text="Title")
        self.tree.heading("platform", text="Platform")
        self.tree.heading("status", text="Status")
        self.tree.heading("progress", text="Progress")
        self.tree.heading("notes", text="Notes")

        self.tree.column("title", width=150)
        self.tree.column("platform", width=100)
        self.tree.column("status", width=100)
        self.tree.column("progress", width=100)
        self.tree.column("notes", width=150)

        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=2, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.button_frame = tk.Frame(self.frame)
        self.button_frame.grid(row=3, column=0, columnspan=2, pady=5, sticky="ew")

        self.add_button = ttk.Button(self.button_frame, text="Add Course", command=self.add_course_dialog)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.edit_button = ttk.Button(self.button_frame, text="Edit Course", command=self.edit_course_dialog)
        self.edit_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = ttk.Button(self.button_frame, text="Delete Course", command=self.delete_course)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.progress_button = ttk.Button(self.button_frame, text="Set Progress", command=self.set_progress_dialog)
        self.progress_button.pack(side=tk.LEFT, padx=5)

        self.notes_button = ttk.Button(self.button_frame, text="Notes", command=self.notes_dialog)
        self.notes_button.pack(side=tk.LEFT, padx=5)

        self.export_button = ttk.Button(self.button_frame, text="Export", command=self.export_to_csv)
        self.export_button.pack(side=tk.LEFT, padx=5)

        self.import_button = ttk.Button(self.button_frame, text="Import", command=self.import_from_csv)
        self.import_button.pack(side=tk.LEFT, padx=5)

        self.reload_button = ttk.Button(self.button_frame, text="Reload", command=self.reload_app)
        self.reload_button.pack(side=tk.LEFT, padx=5)

        self.theme_button = ttk.Button(self.button_frame, text="Toggle Theme", command=self.toggle_theme)
        self.theme_button.pack(side=tk.LEFT, padx=5)

        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        self.update_dashboard()
        self.load_courses()

    def configure_theme(self):
        if self.current_theme == "light":
            self.style.theme_use("clam")
            self.root.configure(bg="#f0f0f0")
            self.frame.configure(bg="#f0f0f0")
            self.dashboard_frame.configure(bg="#e0e0e0")
            self.search_frame.configure(bg="#f0f0f0")
            self.button_frame.configure(bg="#f0f0f0")
            self.total_label.configure(bg="#e0e0e0", fg="black")
            self.completed_label.configure(bg="#e0e0e0", fg="black")
            self.progress_label.configure(bg="#e0e0e0", fg="black")
        else:
            self.style.theme_use("clam")
            self.root.configure(bg="#2d2d2d")
            self.frame.configure(bg="#2d2d2d")
            self.dashboard_frame.configure(bg="#3c3c3c")
            self.search_frame.configure(bg="#2d2d2d")
            self.button_frame.configure(bg="#2d2d2d")
            self.total_label.configure(bg="#3c3c3c", fg="white")
            self.completed_label.configure(bg="#3c3c3c", fg="white")
            self.progress_label.configure(bg="#3c3c3c", fg="white")
            self.style.configure("Treeview", background="#2d2d2d", foreground="white", fieldbackground="#2d2d2d")
            self.style.map("Treeview", background=[("selected", "#4a4a4a")])

    def toggle_theme(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.configure_theme()
        self.load_courses()

    def update_dashboard(self):
        total = len(self.courses_cache)
        completed = sum(1 for course in self.courses_cache if course[3] == "Completed")
        avg_progress = sum(course[4] for course in self.courses_cache) / total if total > 0 else 0

        self.total_label.config(text=f"Total Courses: {total}")
        self.completed_label.config(text=f"Completed: {completed}")
        self.progress_label.config(text=f"Avg Progress: {avg_progress:.1f}%")

    def load_courses(self, filter_text=""):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.courses_cache = list(self.db.get_all_courses())  # Refresh cache
        for course in self.courses_cache:
            notes_preview = course[5][:20] + "..." if course[5] and len(course[5]) > 20 else course[5]
            display_text = f"{course[1]} - {course[2]} ({course[3]}, {course[4]}%) | Notes: {notes_preview}"
            if filter_text.lower() in display_text.lower():
                progress_bar = ttk.Progressbar(self.tree, length=80, maximum=100, value=course[4])
                self.tree.insert("", "end", values=(course[1], course[2], course[3], ""), tags=(course[0],))
                self.tree.window_create(self.tree.get_children()[-1], column=3, window=progress_bar)
                self.tree.set(self.tree.get_children()[-1], "notes", notes_preview)
        self.update_dashboard()

    def filter_courses(self, event):
        filter_text = self.search_entry.get()
        self.load_courses(filter_text)

    def add_course_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Course")
        dialog.geometry("300x200")
        dialog.grab_set()
        dialog.configure(bg="#f0f0f0" if self.current_theme == "light" else "#2d2d2d")

        tk.Label(dialog, text="Course Title:", bg=dialog.cget("bg"), fg="black" if self.current_theme == "light" else "white").pack(pady=5)
        title_entry = tk.Entry(dialog, width=30)
        title_entry.pack()

        tk.Label(dialog, text="Platform:", bg=dialog.cget("bg"), fg="black" if self.current_theme == "light" else "white").pack(pady=5)
        platform_entry = tk.Entry(dialog, width=30)
        platform_entry.pack()

        tk.Label(dialog, text="Notes:", bg=dialog.cget("bg"), fg="black" if self.current_theme == "light" else "white").pack(pady=5)
        notes_entry = tk.Entry(dialog, width=30)
        notes_entry.pack()

        def submit():
            title = title_entry.get().strip()
            platform = platform_entry.get().strip()
            notes = notes_entry.get().strip()
            if title and platform:
                self.db.add_course(title, platform, notes)
                self.load_courses(self.search_entry.get())
                dialog.destroy()
                messagebox.showinfo("Success", f"Added '{title}' from {platform}")
            else:
                messagebox.showwarning("Input Error", "Please fill in title and platform")

        ttk.Button(dialog, text="Submit", command=submit).pack(pady=10)

    def edit_course_dialog(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a course to edit")
            return

        course_id = int(self.tree.item(selected[0], "tags")[0])
        course = self.db.get_course_by_id(course_id)

        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Course")
        dialog.geometry("300x150")
        dialog.grab_set()
        dialog.configure(bg="#f0f0f0" if self.current_theme == "light" else "#2d2d2d")

        tk.Label(dialog, text="Course Title:", bg=dialog.cget("bg"), fg="black" if self.current_theme == "light" else "white").pack(pady=5)
        title_entry = tk.Entry(dialog, width=30)
        title_entry.pack()
        title_entry.insert(0, course[1])

        tk.Label(dialog, text="Platform:", bg=dialog.cget("bg"), fg="black" if self.current_theme == "light" else "white").pack(pady=5)
        platform_entry = tk.Entry(dialog, width=30)
        platform_entry.pack()
        platform_entry.insert(0, course[2])

        def submit():
            title = title_entry.get().strip()
            platform = platform_entry.get().strip()
            if title and platform:
                self.db.update_course(course_id, title=title, platform=platform)
                self.load_courses(self.search_entry.get())
                dialog.destroy()
                messagebox.showinfo("Success", f"Updated course ID {course_id}")
            else:
                messagebox.showwarning("Input Error", "Please fill in both fields")

        ttk.Button(dialog, text="Submit", command=submit).pack(pady=10)

    def delete_course(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a course to delete")
            return

        course_id = int(self.tree.item(selected[0], "tags")[0])
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this course?"):
            self.db.delete_course(course_id)
            self.load_courses(self.search_entry.get())
            messagebox.showinfo("Success", f"Deleted course ID {course_id}")

    def set_progress_dialog(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a course to set progress")
            return

        course_id = int(self.tree.item(selected[0], "tags")[0])
        course = self.db.get_course_by_id(course_id)

        dialog = tk.Toplevel(self.root)
        dialog.title(f"Set Progress for {course[1]}")
        dialog.geometry("300x120")
        dialog.grab_set()
        dialog.configure(bg="#f0f0f0" if self.current_theme == "light" else "#2d2d2d")

        tk.Label(dialog, text=f"Progress (0-100%): Current = {course[4]}%", bg=dialog.cget("bg"), fg="black" if self.current_theme == "light" else "white").pack(pady=5)
        progress_entry = tk.Entry(dialog, width=10)
        progress_entry.pack()
        progress_entry.insert(0, course[4])

        def submit():
            try:
                progress = int(progress_entry.get().strip())
                if 0 <= progress <= 100:
                    self.db.update_course(course_id, progress=progress)
                    status = "Completed" if progress == 100 else "In Progress" if progress > 0 else "Not Started"
                    self.db.update_course(course_id, status=status)
                    self.load_courses(self.search_entry.get())
                    dialog.destroy()
                    messagebox.showinfo("Success", f"Progress set to {progress}% for {course[1]}")
                else:
                    messagebox.showwarning("Input Error", "Progress must be between 0 and 100")
            except ValueError:
                messagebox.showwarning("Input Error", "Please enter a valid number")

        ttk.Button(dialog, text="Submit", command=submit).pack(pady=10)

    def notes_dialog(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a course to add notes")
            return

        course_id = int(self.tree.item(selected[0], "tags")[0])
        course = self.db.get_course_by_id(course_id)

        dialog = tk.Toplevel(self.root)
        dialog.title(f"Notes for {course[1]}")
        dialog.geometry("400x200")
        dialog.grab_set()
        dialog.configure(bg="#f0f0f0" if self.current_theme == "light" else "#2d2d2d")

        tk.Label(dialog, text="Notes:", bg=dialog.cget("bg"), fg="black" if self.current_theme == "light" else "white").pack(pady=5)
        notes_text = tk.Text(dialog, width=40, height=10, bg="white" if self.current_theme == "light" else "#3c3c3c", fg="black" if self.current_theme == "light" else "white")
        notes_text.pack()
        notes_text.insert(tk.END, course[5])

        def submit():
            notes = notes_text.get("1.0", tk.END).strip()
            self.db.update_course(course_id, notes=notes)
            self.load_courses(self.search_entry.get())
            dialog.destroy()
            messagebox.showinfo("Success", f"Notes updated for {course[1]}")

        ttk.Button(dialog, text="Submit", command=submit).pack(pady=10)

    def export_to_csv(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Save Courses As"
        )
        if filename:
            self.db.export_to_csv(filename)
            messagebox.showinfo("Success", f"Courses exported to {filename}")

    def import_from_csv(self):
        filename = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv")],
            title="Import Courses From"
        )
        if filename:
            self.db.close()
            self.db = Database()
            self.db.import_from_csv(filename)
            self.courses_cache = list(self.db.get_all_courses())  # Update cache
            self.load_courses(self.search_entry.get())
            messagebox.showinfo("Success", f"Courses imported from {filename}")

    def reload_app(self):
        self.db.close()
        self.db = Database()
        self.db.import_from_csv()
        self.courses_cache = list(self.db.get_all_courses())  # Update cache
        self.load_courses(self.search_entry.get())
        messagebox.showinfo("Reload", "App reloaded successfully")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    app = CourseApp(root)
    app.run()