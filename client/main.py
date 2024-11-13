from PyQt6.QtWidgets import QApplication
from login_window import LoginWindow


if __name__ == "__main__":
    app = QApplication([])
    login_window = LoginWindow()
    login_window.show()
    app.exec()
