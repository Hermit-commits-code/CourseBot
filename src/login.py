from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox
)
from database import add_user, authenticate_user
from dashboard import DashboardApp


class LoginApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Course Tracker - Login")
        self.setGeometry(100, 100, 400, 300)

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout
        layout = QVBoxLayout()

        # Username
        self.username_label = QLabel("Username:")
        layout.addWidget(self.username_label)
        self.username_input = QLineEdit()
        layout.addWidget(self.username_input)

        # Password
        self.password_label = QLabel("Password:")
        layout.addWidget(self.password_label)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        # Login Button
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        # Register Button
        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.register)
        layout.addWidget(self.register_button)

        self.central_widget.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if authenticate_user(username, password):
            QMessageBox.information(self, "Success", "Login successful!")
            self.dashboard = DashboardApp()
            self.dashboard.show()
            self.close()
        else:
            QMessageBox.critical(self, "Error", "Invalid username or password.")

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()

        try:
            add_user(username, password)
            QMessageBox.information(self, "Success", "Registration successful!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Registration failed: {e}")