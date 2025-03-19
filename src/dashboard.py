from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QMessageBox


class DashboardApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Course Tracker - Dashboard")
        self.setGeometry(100, 100, 600, 400)

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout
        layout = QVBoxLayout()

        # Welcome Message
        self.welcome_label = QLabel("Welcome to the Dashboard!")
        layout.addWidget(self.welcome_label)

        # Logout Button
        self.logout_button = QPushButton("Logout")
        self.logout_button.clicked.connect(self.logout)
        layout.addWidget(self.logout_button)

        self.central_widget.setLayout(layout)

    def logout(self):
        QMessageBox.information(self, "Info", "You have been logged out.")
        from login import LoginApp
        self.login = LoginApp()
        self.login.show()
        self.close()