from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import mysql.connector
from employee_window import EmployeeWindow
from client_window import ClientWindow


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Логин")
        self.layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_button = QPushButton("Войти")

        self.layout.addWidget(QLabel("Логин:"))
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(QLabel("Пароль:"))
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.login_button)

        self.login_button.clicked.connect(self.login)

        # Надпись
        text_label = QLabel("Сервис закупки медикаментов Аптека +")
        text_label.setStyleSheet("color: red")

        # Добавление надписи в компоновку
        self.layout.addWidget(text_label)

        self.setLayout(self.layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Подключение к базе данных
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="sas",
            database="pharmacy"
        )

        cursor = db.cursor()

        # Проверка, является ли входящий пользователь сотрудником
        cursor.execute("SELECT * FROM Employee WHERE Login=%s AND Password=%s", (username, password))
        employee = cursor.fetchone()

        if employee:
            self.employee_window = EmployeeWindow()
            self.employee_window.show()
        else:
            # Проверка, является ли входящий пользователь клиентом
            cursor.execute("SELECT * FROM Client WHERE Login=%s AND Password=%s", (username, password))
            client = cursor.fetchone()

            if client:
                # Передача имени клиента в качестве аргумента
                self.client_window = ClientWindow()
                self.client_window.show()
            else:
                QMessageBox.warning(self, "Ошибка", "Неправильный логин или пароль")
