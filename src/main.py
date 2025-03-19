import sys
from PyQt5.QtWidgets import QApplication
from database import init_db
from login import LoginApp

if __name__ == "__main__":
    init_db()  # Initialize the database

    app = QApplication(sys.argv)
    login = LoginApp()
    login.show()
    sys.exit(app.exec_())