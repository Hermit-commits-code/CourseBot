from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QMessageBox, QTableWidget, QTableWidgetItem
)
from add_course import AddCourseApp
from database import get_courses


class DashboardApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Course Tracker - Dashboard")
        self.setGeometry(100, 100, 800, 600)

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout
        layout = QVBoxLayout()

        # Welcome Message
        self.welcome_label = QLabel("Welcome to the Dashboard!")
        layout.addWidget(self.welcome_label)

        # Add Course Button
        self.add_course_button = QPushButton("Add Course")
        self.add_course_button.clicked.connect(self.open_add_course)
        layout.addWidget(self.add_course_button)

        # Courses Table
        self.courses_table = QTableWidget()
        self.courses_table.setColumnCount(5)
        self.courses_table.setHorizontalHeaderLabels(["Name", "Platform", "Progress", "Start Date", "Notes"])
        layout.addWidget(self.courses_table)

        # Load Courses
        self.load_courses()

        # Logout Button
        self.logout_button = QPushButton("Logout")
        self.logout_button.clicked.connect(self.logout)
        layout.addWidget(self.logout_button)

        self.central_widget.setLayout(layout)

    def load_courses(self):
        """Load courses from the database and display them in the table."""
        courses = get_courses()
        self.courses_table.setRowCount(len(courses))

        for row, course in enumerate(courses):
            self.courses_table.setItem(row, 0, QTableWidgetItem(course[1]))  # Name
            self.courses_table.setItem(row, 1, QTableWidgetItem(course[2]))  # Platform
            self.courses_table.setItem(row, 2, QTableWidgetItem(str(course[3])))  # Progress
            self.courses_table.setItem(row, 3, QTableWidgetItem(course[4]))  # Start Date
            self.courses_table.setItem(row, 4, QTableWidgetItem(course[6]))  # Notes

    def open_add_course(self):
        """Open the Add Course screen."""
        self.add_course_window = AddCourseApp(self)
        self.add_course_window.show()

    def logout(self):
        QMessageBox.information(self, "Info", "You have been logged out.")
        from login import LoginApp
        self.login = LoginApp()
        self.login.show()
        self.close()