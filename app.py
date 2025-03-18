import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from database import init_db, add_user, authenticate_user
from tkinter import messagebox

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Course Tracker - Login")

        # Username
        ttk.Label(root, text="Username:").pack(pady=5)
        self.username_entry = ttk.Entry(root)
        self.username_entry.pack(pady=5)

        # Password
        ttk.Label(root, text="Password:").pack(pady=5)
        self.password_entry = ttk.Entry(root, show="*")
        self.password_entry.pack(pady=5)

        # Login Button
        ttk.Button(root, text="Login", command=self.login).pack(pady=10)

        # Register Button
        ttk.Button(root, text="Register", command=self.register).pack(pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if authenticate_user(username, password):
            messagebox.showinfo("Success", "Login successful!")
            self.root.destroy()
            DashboardApp(ttk.Window(themename="darkly"))
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            add_user(username, password)
            messagebox.showinfo("Success", "Registration successful!")
        except Exception as e:
            messagebox.showerror("Error", f"Registration failed: {e}")

class DashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Course Tracker - Dashboard")

        ttk.Label(root, text="Welcome to the Dashboard!").pack(pady=20)
        ttk.Button(root, text="Logout", command=self.logout).pack(pady=10)

    def logout(self):
        self.root.destroy()
        LoginApp(ttk.Window(themename="darkly"))

# Initialize the database
init_db()

# Run the application
if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    LoginApp(root)
    root.mainloop()