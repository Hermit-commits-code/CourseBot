import tkinter as tk
from tkinter import ttk
from data.database import Database
from tkinter import messagebox, filedialog

class CourseApp:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.root.title("Course Tracking App")
        self.create_widgets()
        self.refresh_course_list()

    def create_widgets(self):
        self.tree = ttk.Treeview(self.root, columns=("ID", "Title", "Platform", "Status", "Progress", "Notes"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Platform", text="Platform")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Progress", text="Progress")
        self.tree.heading("Notes", text="Notes")
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.add_btn = tk.Button(self.root, text="Add Course", command=self.add_course)
        self.add_btn.pack(side=tk.LEFT, padx=10, pady=10)

        self.update_btn = tk.Button(self.root, text="Update Course", command=self.update_course)
        self.update_btn.pack(side=tk.LEFT, padx=10, pady=10)

        self.delete_btn = tk.Button(self.root, text="Delete Course", command=self.delete_course)
        self.delete_btn.pack(side=tk.LEFT, padx=10, pady=10)

        self.export_btn = tk.Button(self.root, text="Export to CSV", command=self.export_to_csv)
        self.export_btn.pack(side=tk.LEFT, padx=10, pady=10)

        self.import_btn = tk.Button(self.root, text="Import from CSV", command=self.import_from_csv)
        self.import_btn.pack(side=tk.LEFT, padx=10, pady=10)

    def refresh_course_list(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for course in self.db.get_all_courses():
            self.tree.insert("", "end", values=course)

    def add_course(self):
        self.course_form("Add Course")

    def update_course(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "No course selected")
            return
        course_id = self.tree.item(selected_item[0], "values")[0]
        self.course_form("Update Course", course_id)

    def delete_course(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "No course selected")
            return
        course_id = self.tree.item(selected_item[0], "values")[0]
        self.db.delete_course(course_id)
        self.refresh_course_list()

    def export_to_csv(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if filename:
            self.db.export_to_csv(filename)
            messagebox.showinfo("Success", f"Exported to {filename}")

    def import_from_csv(self):
        filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if filename:
            self.db.import_from_csv(filename)
            self.refresh_course_list()
            messagebox.showinfo("Success", f"Imported from {filename}")

    def course_form(self, title, course_id=None):
        form = tk.Toplevel(self.root)
        form.title(title)

        tk.Label(form, text="Title:").grid(row=0, column=0, padx=10, pady=5)
        title_entry = tk.Entry(form)
        title_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form, text="Platform:").grid(row=1, column=0, padx=10, pady=5)
        platform_entry = tk.Entry(form)
        platform_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(form, text="Status:").grid(row=2, column=0, padx=10, pady=5)
        status_combobox = ttk.Combobox(form, values=["Not Started", "In Progress", "Completed"])
        status_combobox.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(form, text="Progress:").grid(row=3, column=0, padx=10, pady=5)
        progress_entry = tk.Entry(form)
        progress_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(form, text="Notes:").grid(row=4, column=0, padx=10, pady=5)
        notes_entry = tk.Entry(form)
        notes_entry.grid(row=4, column=1, padx=10, pady=5)

        if course_id:
            course = self.db.get_course_by_id(course_id)
            title_entry.insert(0, course[1])
            platform_entry.insert(0, course[2])
            status_combobox.set(course[3])
            progress_entry.insert(0, course[4])
            notes_entry.insert(0, course[5])

        def save_course():
            title = title_entry.get()
            platform = platform_entry.get()
            status = status_combobox.get()
            progress = progress_entry.get()
            notes = notes_entry.get()
            if not title or not platform:
                messagebox.showwarning("Warning", "Title and Platform are required")
                return
            try:
                progress = int(progress)
            except ValueError:
                messagebox.showwarning("Warning", "Progress must be an integer")
                return
            if not 0 <= progress <= 100:
                messagebox.showwarning("Warning", "Progress must be between 0 and 100")
                return
            if course_id:
                self.db.update_course(course_id, title, platform, status, progress, notes)
            else:
                self.db.add_course(title, platform, notes)
            self.refresh_course_list()
            form.destroy()

        save_btn = tk.Button(form, text="Save", command=save_course)
        save_btn.grid(row=5, column=0, columnspan=2, pady=10)

    def run(self):
        self.root.mainloop()