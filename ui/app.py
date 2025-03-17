import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
from tkinter import ttk
from data.database import Database

class CourseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Course Tracker")
        self.db = Database()
        try:
            self.db.import_from_csv()
        except ValueError as e:
            messagebox.showerror("Startup Error", str(e))
        self.courses_cache = list(self.db.get_all_courses())
        self.sort_column = "title"  # Default sort
        self.sort_reverse = False

        self.style = ttk.Style()
        self.current_theme = "light"

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

        self.tree.heading("title", text="Title", command=lambda: self.sort_treeview("title"))
        self.tree.heading("platform", text="Platform", command=lambda: self.sort_treeview("platform"))
        self.tree.heading("status", text="Status", command=lambda: self.sort_treeview("status"))
        self.tree.heading("progress", text="Progress", command=lambda: self.sort_treeview("progress"))
        self.tree.heading("notes", text="Notes", command=lambda: self.sort_treeview("notes"))

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

        self.configure_theme()
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

    def sort_treeview(self, column):
        if self.sort_column == column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = column
            self.sort_reverse = False
        self.load_courses(self.search_entry.get())

    def update_dashboard(self):
        try:
            total = len(self.courses_cache)
            completed = sum(1 for course in self.courses_cache if course[3] == "Completed")
            avg_progress = sum(course[4] for course in self.courses_cache) / total if total > 0 else 0
            self.total_label.config(text=f"Total Courses: {total}")
            self.completed_label.config(text=f"Completed: {completed}")
            self.progress_label.config(text=f"Avg Progress: {avg_progress:.1f}%")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update dashboard: {e}")

    def load_courses(self, filter_text=""):
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)
            self.courses_cache = list(self.db.get_all_courses())
            column_indices = {"title": 1, "platform": 2, "status": 3, "progress": 4, "notes": 5}
            self.courses_cache.sort(key=lambda x: x[column_indices[self.sort_column]], reverse=self.sort_reverse)
            if self.sort_column == "progress":  # Special case for numeric sort
                self.courses_cache.sort(key=lambda x: int(x[4]), reverse=self.sort_reverse)
            for course in self.courses_cache:
                notes_preview = course[5][:20] + "..." if course[5] and len(course[5]) > 20 else course[5]
                display_text = f"{course[1]} - {course[2]} ({course[3]}, {course[4]}%) | Notes: {notes_preview}"
                if filter_text.lower() in display_text.lower():
                    progress_text = f"{course[4]}%"
                    self.tree.insert("", "end", values=(course[1], course[2], course[3], progress_text, notes_preview), tags=(course[0],))
            self.update_dashboard()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def filter_courses(self, event):
        self.load_courses(self.search_entry.get())

    def add_course_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Course")
        dialog.geometry("400x250")
        dialog.grab_set()
        dialog.configure(bg="#f0f0f0" if self.current_theme == "light" else "#2d2d2d")

        frame = tk.Frame(dialog, bg=dialog.cget("bg"))
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        tk.Label(frame, text="Course Title:", bg=frame.cget("bg"), fg="black" if self.current_theme == "light" else "white").grid(row=0, column=0, pady=5, sticky="w")
        title_entry = tk.Entry(frame, width=40)
        title_entry.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Platform:", bg=frame.cget("bg"), fg="black" if self.current_theme == "light" else "white").grid(row=1, column=0, pady=5, sticky="w")
        platform_entry = tk.Entry(frame, width=40)
        platform_entry.grid(row=1, column=1, pady=5)

        tk.Label(frame, text="Notes:", bg=frame.cget("bg"), fg="black" if self.current_theme == "light" else "white").grid(row=2, column=0, pady=5, sticky="w")
        notes_entry = tk.Entry(frame, width=40)
        notes_entry.grid(row=2, column=1, pady=5)

        def submit():
            title = title_entry.get().strip()
            platform = platform_entry.get().strip()
            notes = notes_entry.get().strip()
            if not title or not platform:
                messagebox.showwarning("Input Error", "Title and platform are required")
                return
            try:
                self.db.add_course(title, platform, notes)
                self.load_courses(self.search_entry.get())
                dialog.destroy()
                messagebox.showinfo("Success", f"Added '{title}' from {platform}")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        submit_button = ttk.Button(frame, text="Submit", command=submit)
        submit_button.grid(row=3, column=0, columnspan=2, pady=20)

    def edit_course_dialog(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a course to edit")
            return

        course_id = int(self.tree.item(selected[0], "tags")[0])
        try:
            course = self.db.get_course_by_id(course_id)
            if not course:
                messagebox.showerror("Error", f"Course ID {course_id} not found")
                return

            dialog = tk.Toplevel(self.root)
            dialog.title("Edit Course")
            dialog.geometry("400x200")
            dialog.grab_set()
            dialog.configure(bg="#f0f0f0" if self.current_theme == "light" else "#2d2d2d")

            frame = tk.Frame(dialog, bg=dialog.cget("bg"))
            frame.pack(padx=20, pady=20, fill="both", expand=True)

            tk.Label(frame, text="Course Title:", bg=frame.cget("bg"), fg="black" if self.current_theme == "light" else "white").grid(row=0, column=0, pady=5, sticky="w")
            title_entry = tk.Entry(frame, width=40)
            title_entry.grid(row=0, column=1, pady=5)
            title_entry.insert(0, course[1])

            tk.Label(frame, text="Platform:", bg=frame.cget("bg"), fg="black" if self.current_theme == "light" else "white").grid(row=1, column=0, pady=5, sticky="w")
            platform_entry = tk.Entry(frame, width=40)
            platform_entry.grid(row=1, column=1, pady=5)
            platform_entry.insert(0, course[2])

            def submit():
                title = title_entry.get().strip()
                platform = platform_entry.get().strip()
                if not title or not platform:
                    messagebox.showwarning("Input Error", "Title and platform are required")
                    return
                try:
                    self.db.update_course(course_id, title=title, platform=platform)
                    self.load_courses(self.search_entry.get())
                    dialog.destroy()
                    messagebox.showinfo("Success", f"Updated course ID {course_id}")
                except ValueError as e:
                    messagebox.showerror("Error", str(e))

            submit_button = ttk.Button(frame, text="Submit", command=submit)
            submit_button.grid(row=2, column=0, columnspan=2, pady=20)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def delete_course(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a course to delete")
            return

        course_id = int(self.tree.item(selected[0], "tags")[0])
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this course?"):
            try:
                self.db.delete_course(course_id)
                self.load_courses(self.search_entry.get())
                messagebox.showinfo("Success", f"Deleted course ID {course_id}")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def set_progress_dialog(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a course to set progress")
            return

        course_id = int(self.tree.item(selected[0], "tags")[0])
        try:
            course = self.db.get_course_by_id(course_id)
            if not course:
                messagebox.showerror("Error", f"Course ID {course_id} not found")
                return

            dialog = tk.Toplevel(self.root)
            dialog.title(f"Set Progress for {course[1]}")
            dialog.geometry("400x150")
            dialog.grab_set()
            dialog.configure(bg="#f0f0f0" if self.current_theme == "light" else "#2d2d2d")

            frame = tk.Frame(dialog, bg=dialog.cget("bg"))
            frame.pack(padx=20, pady=20, fill="both", expand=True)

            tk.Label(frame, text=f"Progress (0-100%): Current = {course[4]}%", bg=frame.cget("bg"), fg="black" if self.current_theme == "light" else "white").grid(row=0, column=0, pady=5, sticky="w")
            progress_entry = tk.Entry(frame, width=10)
            progress_entry.grid(row=0, column=1, pady=5)
            progress_entry.insert(0, course[4])

            def submit():
                try:
                    progress = int(progress_entry.get().strip())
                    if not 0 <= progress <= 100:
                        messagebox.showwarning("Input Error", "Progress must be between 0 and 100")
                        return
                    self.db.update_course(course_id, progress=progress)
                    status = "Completed" if progress == 100 else "In Progress" if progress > 0 else "Not Started"
                    self.db.update_course(course_id, status=status)
                    self.load_courses(self.search_entry.get())
                    dialog.destroy()
                    messagebox.showinfo("Success", f"Progress set to {progress}% for {course[1]}")
                except ValueError as e:
                    if "invalid literal" in str(e):
                        messagebox.showwarning("Input Error", "Please enter a valid number")
                    else:
                        messagebox.showerror("Error", str(e))

            submit_button = ttk.Button(frame, text="Submit", command=submit)
            submit_button.grid(row=1, column=0, columnspan=2, pady=20)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def notes_dialog(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a course to add notes")
            return

        course_id = int(self.tree.item(selected[0], "tags")[0])
        try:
            course = self.db.get_course_by_id(course_id)
            if not course:
                messagebox.showerror("Error", f"Course ID {course_id} not found")
                return

            dialog = tk.Toplevel(self.root)
            dialog.title(f"Notes for {course[1]}")
            dialog.geometry("400x300")
            dialog.grab_set()
            dialog.configure(bg="#f0f0f0" if self.current_theme == "light" else "#2d2d2d")

            frame = tk.Frame(dialog, bg=dialog.cget("bg"))
            frame.pack(padx=20, pady=20, fill="both", expand=True)

            tk.Label(frame, text="Notes:", bg=frame.cget("bg"), fg="black" if self.current_theme == "light" else "white").grid(row=0, column=0, pady=5, sticky="nw")
            notes_text = tk.Text(frame, width=40, height=10, bg="white" if self.current_theme == "light" else "#3c3c3c", fg="black" if self.current_theme == "light" else "white")
            notes_text.grid(row=1, column=0, columnspan=2, pady=5)
            notes_text.insert(tk.END, course[5])

            def submit():
                notes = notes_text.get("1.0", tk.END).strip()
                try:
                    self.db.update_course(course_id, notes=notes)
                    self.load_courses(self.search_entry.get())
                    dialog.destroy()
                    messagebox.showinfo("Success", f"Notes updated for {course[1]}")
                except ValueError as e:
                    messagebox.showerror("Error", str(e))

            submit_button = ttk.Button(frame, text="Submit", command=submit)
            submit_button.grid(row=2, column=0, columnspan=2, pady=20)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def export_to_csv(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Save Courses As"
        )
        if filename:
            try:
                self.db.export_to_csv(filename)
                messagebox.showinfo("Success", f"Courses exported to {filename}")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def import_from_csv(self):
        filename = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv")],
            title="Import Courses From"
        )
        if filename:
            try:
                self.db.close()
                self.db = Database()
                count = self.db.import_from_csv(filename)
                self.courses_cache = list(self.db.get_all_courses())
                self.load_courses(self.search_entry.get())
                messagebox.showinfo("Success", f"Imported {count} courses from {filename}")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def reload_app(self):
        try:
            self.db.close()
            self.db = Database()
            self.db.import_from_csv()
            self.courses_cache = list(self.db.get_all_courses())
            self.load_courses(self.search_entry.get())
            messagebox.showinfo("Reload", "App reloaded successfully")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    app = CourseApp(root)
    app.run()