from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLabel, QScrollArea, QPushButton, QDialog, QFormLayout, QLineEdit
from PyQt6.QtGui import QPixmap
import mysql.connector
from datetime import datetime


class EmployeeList(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Список сотрудников онлайн аптеки")

        self.layout = QVBoxLayout()

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        content_widget = QWidget()
        scroll_layout = QVBoxLayout(content_widget)

        scroll_area.setWidget(content_widget)
        self.layout.addWidget(scroll_area)

        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="sas",
            database="pharmacy"
        )

        add_employee_button = QPushButton("Добавить сотрудника")
        add_employee_button.clicked.connect(self.add_employee_dialog)
        self.layout.addWidget(add_employee_button)

        self.update_employee_list()

        self.setLayout(self.layout)

    def update_employee_list(self):
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)

        cursor = self.db.cursor()

        cursor.execute(
            "SELECT Fullname, Post, Birthdate, Dateofhiring, Phonenumber, Education, Salary, Photo FROM Employee"
        )
        employees = cursor.fetchall()

        for employee in employees:
            employee_widget = QWidget()
            employee_layout = QHBoxLayout()
            employee_label = QLabel()
            photo_path = employee[7]
            photo_pixmap = QPixmap(photo_path)
            employee_label.setPixmap(photo_pixmap)
            employee_info = f"""
                ФИО: {employee[0]}
                Должность: {employee[1]}
                Дата рождения: {employee[2].strftime("%d.%m.%Y")}
                Дата приема на работу: {employee[3].strftime("%d.%m.%Y")}
                Телефонный номер: {employee[4]}
                Образование: {employee[5]}
                Зарплата: {employee[6]} руб.
            """
            employee_text = QTextEdit()
            employee_text.setMarkdown(employee_info)
            employee_layout.addWidget(employee_label)
            employee_layout.addWidget(employee_text)
            employee_widget.setLayout(employee_layout)
            self.layout.addWidget(employee_widget)
            self.layout.addLayout(employee_layout)

        self.layout.update()

    def add_employee_dialog(self):
        add_employee_dialog = AddEmployeeDialog(self)
        add_employee_dialog.exec()


class AddEmployeeDialog(QDialog):
    def __init__(self, employee_list):
        super().__init__()
        self.setWindowTitle('Добавить сотрудника')

        self.employee_list = employee_list

        self.fullname_label = QLabel('ФИО:')
        self.fullname_input = QLineEdit()

        self.post_label = QLabel('Должность:')
        self.post_input = QLineEdit()

        self.login_label = QLabel('Логин:')
        self.login_input = QLineEdit()

        self.password_label = QLabel('Пароль:')
        self.password_input = QLineEdit()

        self.birthdate_label = QLabel('Дата рождения:')
        self.birthdate_input = QLineEdit()

        self.dateofhiring_label = QLabel('Дата приема на работу:')
        self.dateofhiring_input = QLineEdit()

        self.phonenumber_label = QLabel('Телефонный номер:')
        self.phonenumber_input = QLineEdit()

        self.education_label = QLabel('Образование:')
        self.education_input = QLineEdit()

        self.salary_label = QLabel('Зарплата:')
        self.salary_input = QLineEdit()

        self.photo_label = QLabel('Путь к изображению:')
        self.photo_input = QLineEdit()

        self.add_employee_button = QPushButton('Добавить сотрудника')
        self.add_employee_button.clicked.connect(self.add_employee)

        layout = QFormLayout(self)
        layout.addRow(self.fullname_label, self.fullname_input)
        layout.addRow(self.post_label, self.post_input)
        layout.addRow(self.login_label, self.login_input)
        layout.addRow(self.password_label, self.password_input)
        layout.addRow(self.birthdate_label, self.birthdate_input)
        layout.addRow(self.dateofhiring_label, self.dateofhiring_input)
        layout.addRow(self.phonenumber_label, self.phonenumber_input)
        layout.addRow(self.education_label, self.education_input)
        layout.addRow(self.salary_label, self.salary_input)
        layout.addRow(self.photo_label, self.photo_input)
        layout.addRow(self.add_employee_button)

    def add_employee(self):
        fullname = self.fullname_input.text()
        post = self.post_input.text()
        login = self.login_input.text()
        password = self.password_input.text()
        birthdate = datetime.strptime(self.birthdate_input.text(), "%d.%m.%Y")
        dateofhiring = datetime.strptime(self.dateofhiring_input.text(), "%d.%m.%Y")
        phonenumber = self.phonenumber_input.text()
        education = self.education_input.text()
        salary = float(self.salary_input.text())
        photo_path = self.photo_input.text()

        cursor = self.employee_list.db.cursor()
        cursor.execute(
            "INSERT INTO Employee (Fullname, Post, Login, Password, Birthdate, Dateofhiring, Phonenumber, Education, Salary, Photo) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (fullname, post, login, password, birthdate, dateofhiring, phonenumber, education, salary, photo_path)
        )

        self.employee_list.db.commit()
        self.employee_list.update_employee_list()
        self.accept()

