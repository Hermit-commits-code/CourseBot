import tkinter as tk
from tkinter import ttk, simpledialog, filedialog
from tkinter import messagebox
import sqlite3
from datetime import datetime, timedelta
from data.database import Database
from report_generator import ReportGenerator

class CourseApp:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.user_id = None
        self.root.title("Course Tracking App")
        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Username:").pack(pady=10)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)
        tk.Label(self.root, text="Password:").pack(pady=10)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)
        tk.Button(self.root, text="Login", command=self.login).pack(pady=5)
        tk.Button(self.root, text="Register", command=self.register).pack(pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showwarning("Warning", "Username and Password are required")
            return
        user = self.db.get_user(username, password)
        if user:
            self.user_id = user[0]
            self.create_main_screen()
            self.check_reminders()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showwarning("Warning", "Username and Password are required")
            return
        try:
            self.db.add_user(username, password)
            user = self.db.get_user(username, password)
            self.user_id = user[0]
            self.db.add_user_settings(self.user_id)
            self.create_main_screen()
            self.check_reminders()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def create_main_screen(self):
        self.clear_screen()
        self.create_widgets()
        self.refresh_course_list()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

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
        
        self.export_btn = tk.Button(self.root, text="Export to CSV", command=self.export_to_csv)
        self.export_btn.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.import_btn = tk.Button(self.root, text="Import from CSV", command=self.import_from_csv)
        self.import_btn.pack(side=tk.LEFT, padx=10, pady=10)

        self.reminder_btn = tk.Button(self.root, text="Set Reminder", command=self.set_reminder)
        self.reminder_btn.pack(side=tk.LEFT, padx=10, pady=10)

        self.report_btn = tk.Button(self.root, text="Generate Report", command=self.generate_report)
        self.report_btn.pack(side=tk.LEFT, padx=10, pady=10)

    def refresh_course_list(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for course in self.db.get_all_courses(self.user_id):
            self.tree.insert("", "end", values=course)

    def add_course(self):
        form = tk.Toplevel(self.root)
        form.title("Add Course")

        tk.Label(form, text="Title:").grid(row=0, column=0, padx=10, pady=5)
        title_entry = tk.Entry(form)
        title_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form, text="Platform:").grid(row=1, column=0, padx=10, pady=5)
        platform_entry = tk.Entry(form)
        platform_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(form, text="Notes:").grid(row=2, column=0, padx=10, pady=5)
        notes_entry = tk.Entry(form)
        notes_entry.grid(row=2, column=1, padx=10, pady=5)

        def save_course():
            title = title_entry.get()
            platform = platform_entry.get()
            notes = notes_entry.get()
            if not title or not platform:
                tk.messagebox.showwarning("Warning", "Title and Platform are required")
                return
            self.db.add_course(self.user_id, title, platform, notes)
            self.refresh_course_list()
            form.destroy()

        save_btn = tk.Button(form, text="Save", command=save_course)
        save_btn.grid(row=3, column=0, columnspan=2, pady=10)

    def export_to_csv(self):
        try:
            filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if filename:
                self.db.export_to_csv(self.user_id, filename)
                messagebox.showinfo("Success", f"Exported to {filename} successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export to CSV: {e}")

    def import_from_csv(self):
        try:
            filename = filedialog.askopenfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if filename:
                self.db.import_from_csv(self.user_id, filename)
                self.refresh_course_list()
                messagebox.showinfo("Success", f"Imported from {filename} successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import from CSV: {e}")

    def generate_report(self):
        try:
            report_generator = ReportGenerator(self.db)
            report_generator.generate_course_report(self.user_id)
            messagebox.showinfo("Success", "Report generated successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {e}")

    def set_reminder(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a course to set a reminder")
            return
        course_id = self.tree.item(selected_item[0], "values")[0]
        form = tk.Toplevel(self.root)
        form.title("Set Reminder")

        tk.Label(form, text="Reminder Date (YYYY-MM-DD):").grid(row=0, column=0, padx=10, pady=5)
        date_entry = tk.Entry(form)
        date_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form, text="Message:").grid(row=1, column=0, padx=10, pady=5)
        message_entry = tk.Entry(form)
        message_entry.grid(row=1, column=1, padx=10, pady=5)

        def save_reminder():
            reminder_date = date_entry.get()
            message = message_entry.get()
            try:
                datetime.strptime(reminder_date, "%Y-%m-%d")  # Validate date format
                self.db.add_reminder(self.user_id, course_id, reminder_date, message)
                messagebox.showinfo("Success", "Reminder set successfully")
                form.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD")

        save_btn = tk.Button(form, text="Save", command=save_reminder)
        save_btn.grid(row=2, column=0, columnspan=2, pady=10)

    def run(self):
        self.root.after(1000, self.check_reminders)  # Check reminders after 1 second
        self.root.mainloop()

    def check_reminders(self):
        reminders = self.db.get_reminders(self.user_id)
        today = datetime.today().strftime("%Y-%m-%d")
        for reminder in reminders:
            if reminder[3] == today:
                messagebox.showinfo("Reminder", f"{reminder[4]}")
        self.root.after(60000, self.check_reminders)  # Check reminders every 60 seconds

if __name__ == "__main__":
    root = tk.Tk()
    db = Database("courses.db")
    app = CourseApp(root, db)
    app.run()
    db.close()