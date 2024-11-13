from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QLabel, QMainWindow, QDialog, QTextBrowser
from PyQt6.QtGui import QPixmap, QAction
from employee_list import EmployeeList
from employee_medications import MedicationList


class EmployeeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Окно Администратора")

        # Создание меню
        menubar = self.menuBar()

        # Меню "Файл"
        file_menu = menubar.addMenu('Файл')

        # Пункт меню "Справка"
        help_action = QAction('Справка', self)
        help_action.triggered.connect(self.show_help)
        file_menu.addAction(help_action)

        # Пункт меню "О приложении"
        about_action = QAction('О приложении', self)
        about_action.triggered.connect(self.show_about)
        file_menu.addAction(about_action)

        # Пункт меню "Руководство пользователя"
        user_guide_action = QAction('Руководство пользователя', self)
        user_guide_action.triggered.connect(self.show_user_guide)
        file_menu.addAction(user_guide_action)

        self.layout = QVBoxLayout()

        # Кнопки
        medications_button = QPushButton("Медикаменты")
        employees_button = QPushButton("Наши сотрудники")

        # Добавление кнопок в компоновку
        self.layout.addWidget(medications_button)
        self.layout.addWidget(employees_button)

        # Загрузка и отображение картинки
        image_label = QLabel()
        pixmap = QPixmap("C:\\Users\\122\\PycharmProjects\\app_k\\imgs\\эмбл.png")
        image_label.setPixmap(pixmap)

        # Надпись
        text_label = QLabel("Сервис закупки медикаментов Аптека +")
        text_label.setStyleSheet("color: red")

        # Добавление картинки и надписи в компоновку
        self.layout.addWidget(image_label)
        self.layout.addWidget(text_label)

        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

        # Обработка нажатия на кнопку "Наши сотрудники"
        employees_button.clicked.connect(self.show_employee_list)
        # Обработка нажатия на кнопку "Медикаменты"
        medications_button.clicked.connect(self.show_employee_medications)

    # Метод для отображения справки
    def show_help(self):
        help_dialog = HelpDialog()
        help_dialog.exec()

    # Метод для отображения информации о приложении
    def show_about(self):
        about_dialog = AboutDialog()
        about_dialog.exec()

    # Метод для отображения руководства пользователя
    def show_user_guide(self):
        user_guide_dialog = UserGuideDialog()
        user_guide_dialog.exec()

    # Метод для отображения списка медикаментов сотрудника
    def show_employee_medications(self):
        if not hasattr(self, 'employee_medications'):
            self.employee_medications = MedicationList()
        self.employee_medications.show()

    # Метод для отображения списка сотрудников
    def show_employee_list(self):
        if not hasattr(self, 'employee_list'):
            self.employee_list = EmployeeList()
        self.employee_list.show()


# Класс для отображения руководства пользователя
class UserGuideDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Руководство пользователя')

        text_browser = QTextBrowser()
        text_browser.setPlainText(self.load_user_guide_text())
        text_browser.setReadOnly(True)

        layout = QVBoxLayout(self)
        layout.addWidget(text_browser)

    # Метод для загрузки текста руководства пользователя из файла
    def load_user_guide_text(self):
        try:
            with open('user_guide.txt', 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            return 'Руководство пользователя не найдено.'


# Класс для отображения справки
class HelpDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Справка')

        text_browser = QTextBrowser()
        text_browser.setPlainText(self.load_help_text())
        text_browser.setReadOnly(True)

        layout = QVBoxLayout(self)
        layout.addWidget(text_browser)

    # Метод для загрузки текста справки из файла
    def load_help_text(self):
        try:
            with open('help.txt', 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            return 'Справка не найдена.'


# Класс для отображения информации о приложении
class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('О приложении')

        text_browser = QTextBrowser()
        text_browser.setPlainText(self.load_about_text())
        text_browser.setReadOnly(True)

        layout = QVBoxLayout(self)
        layout.addWidget(text_browser)

    # Метод для загрузки текста об информации о приложении из файла
    def load_about_text(self):
        try:
            with open('about.txt', 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            return 'Информация о приложении не найдена.'




