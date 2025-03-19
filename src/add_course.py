from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox, QDateEdit
)
from database import add_course


class AddCourseApp(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Course")
        self.setGeometry(100, 100, 400, 400)

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout
        layout = QVBoxLayout()

        # Course Name
        self.name_label = QLabel("Course Name:")
        layout.addWidget(self.name_label)
        self.name_input = QLineEdit()
        layout.addWidget(self.name_input)

        # Platform
        self.platform_label = QLabel("Platform:")
        layout.addWidget(self.platform_label)
        self.platform_input = QLineEdit()
        layout.addWidget(self.platform_input)

        # Progress
        self.progress_label = QLabel("Progress (%):")
        layout.addWidget(self.progress_label)
        self.progress_input = QLineEdit()
        layout.addWidget(self.progress_input)

        # Start Date
        self.start_date_label = QLabel("Start Date:")
        layout.addWidget(self.start_date_label)
        self.start_date_input = QDateEdit()
        self.start_date_input.setCalendarPopup(True)
        layout.addWidget(self.start_date_input)

        # Completion Date
        self.completion_date_label = QLabel("Completion Date:")
        layout.addWidget(self.completion_date_label)
        self.completion_date_input = QDateEdit()
        self.completion_date_input.setCalendarPopup(True)
        layout.addWidget(self.completion_date_input)

        # Notes
        self.notes_label = QLabel("Notes:")
        layout.addWidget(self.notes_label)
        self.notes_input = QLineEdit()
        layout.addWidget(self.notes_input)

        # Add Course Button
        self.add_course_button = QPushButton("Add Course")
        self.add_course_button.clicked.connect(self.add_course)
        layout.addWidget(self.add_course_button)

        # Back Button
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.close)
        layout.addWidget(self.back_button)

        self.central_widget.setLayout(layout)

    def add_course(self):
        """Add the course to the database."""
        name = self.name_input.text()
        platform = self.platform_input.text()
        progress = self.progress_input.text()
        start_date = self.start_date_input.text()
        completion_date = self.completion_date_input.text()
        notes = self.notes_input.text()

        if not name or not platform:
            QMessageBox.critical(self, "Error", "Course Name and Platform are required!")
            return

        try:
            add_course(name, platform, progress, start_date, completion_date, notes)
            QMessageBox.information(self, "Success", "Course added successfully!")
            self.close()  # Close the Add Course window
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add course: {e}")