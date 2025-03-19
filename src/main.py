# src/main.py

"""
This is the main entry point for the Budget App application.

This script initializes the PyQt6 application, creates the main application window,
and starts the application's event loop.
"""

import sys  # Import the sys module for system-specific functions
from PyQt6.QtWidgets import QApplication, QWidget  # Import necessary PyQt6 classes
from PyQt6.QtCore import Qt  # Import Qt module, to use its constants.


class MainWindow(QWidget):
    """
    The main window of the Budget App application.

    This class represents the main application window. It inherits from QWidget,
    the base class for all user interface objects in PyQt6.
    """

    def __init__(self):
        """
        Initializes the main window.

        This method sets the window title, initial size, background color, and style.
        """
        super().__init__()  # Call the constructor of the parent class (QWidget)
        self.setWindowTitle("Budget App")  # Set the title of the window
        self.resize(800, 600)  # Set the initial size of the window to 800x600 pixels
        self.setStyleSheet(
            "background-color: #2b2b2b;"
        )  # Set background dark gray using a style sheet
        self.setAttribute(
            Qt.WidgetAttribute.WA_StyledBackground
        )  # allows the background color to be set by the style sheet

# Entry point of the application
if __name__ == "__main__":
    """
    The main execution block of the Budget App.

    This block is executed when the script is run directly. It initializes the
    application, creates the main window, shows the window, and starts the event loop.
    """
    app = QApplication(
        sys.argv
    )  # Create the application instance, passing command-line arguments
    window = MainWindow()  # Create an instance of our main window
    window.show()  # Show the main window
    sys.exit(app.exec())  # Start the application's event loop and exit when the app closes
