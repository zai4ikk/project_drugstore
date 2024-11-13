from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLabel, QScrollArea
from PyQt6.QtGui import QPixmap
import mysql.connector


class EmployeeListForClient(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Список сотрудников онлайн аптеки")

        self.layout = QVBoxLayout()

        # Создание области прокрутки для отображения информации о медикаментах
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Создание виджета для размещения макета информации о медикаментах
        content_widget = QWidget()
        scroll_layout = QVBoxLayout(content_widget)

        # Добавление content_widget в область прокрутки
        scroll_area.setWidget(content_widget)

        # Добавление области прокрутки в основной макет
        self.layout.addWidget(scroll_area)

        # Подключение к базе данных
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="sas",
            database="pharmacy"
        )
        cursor = db.cursor()

        # Получение данных из таблицы Employee
        cursor.execute("SELECT Fullname, Post, Birthdate, Dateofhiring, Phonenumber, Education, Salary, Photo FROM Employee")
        employees = cursor.fetchall()

        # Отображение данных
        for employee in employees:
            employee_widget = QWidget()
            employee_layout = QHBoxLayout()
            employee_label = QLabel()
            photo_path = employee[7]  # путь к изображению из базы данных
            photo_pixmap = QPixmap(photo_path)
            employee_label.setPixmap(photo_pixmap)
            employee_info = f"""
                ФИО: {employee[0]}
                Должность: {employee[1]}
            """
            employee_text = QTextEdit()
            employee_text.setMarkdown(employee_info)
            employee_layout.addWidget(employee_label)
            employee_layout.addWidget(employee_text)
            employee_widget.setLayout(employee_layout)
            self.layout.addWidget(employee_widget)
            scroll_layout.addLayout(employee_layout)

        self.setLayout(self.layout)