from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QLabel, QMainWindow, QDialog, QTextBrowser
from PyQt6.QtGui import QPixmap, QAction
from employee_window import HelpDialog, AboutDialog, UserGuideDialog
from client_medications import ClientMedicationList
from employee_list_for_client import EmployeeListForClient


class ClientWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Окно Сотрудника")

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
        employees_button.clicked.connect(self.show_employee_list_for_client)
        # Обработка нажатия на кнопку "Медикаменты"
        medications_button.clicked.connect(self.show_client_medications)

    def show_help(self):
        help_dialog = HelpDialog()
        help_dialog.exec()

    def show_about(self):
        about_dialog = AboutDialog()
        about_dialog.exec()

    def show_user_guide(self):
        user_guide_dialog = UserGuideDialog()
        user_guide_dialog.exec()

    def show_client_medications(self):
        if not hasattr(self, 'client_medications'):
            self.client_medications = ClientMedicationList()
        self.client_medications.show()

    def show_employee_list_for_client(self):
        if not hasattr(self, 'employee_list_for_client'):
            self.employee_list_for_client = EmployeeListForClient()
        self.employee_list_for_client.show()

    class UserGuideDialog(QDialog):
        def __init__(self):
            super().__init__()
            self.setWindowTitle('Руководство пользователя')

            text_browser = QTextBrowser()
            text_browser.setPlainText(self.load_user_guide_text())
            text_browser.setReadOnly(True)

            layout = QVBoxLayout(self)
            layout.addWidget(text_browser)

        def load_user_guide_text(self):
            try:
                with open('user_guide.txt', 'r', encoding='utf-8') as file:
                    return file.read()
            except FileNotFoundError:
                return 'Руководство пользователя не найдено.'

    class HelpDialog(QDialog):
        def __init__(self):
            super().__init__()
            self.setWindowTitle('Справка')

            text_browser = QTextBrowser()
            text_browser.setPlainText(self.load_help_text())
            text_browser.setReadOnly(True)

            layout = QVBoxLayout(self)
            layout.addWidget(text_browser)

        def load_help_text(self):
            try:
                with open('help.txt', 'r', encoding='utf-8') as file:
                    return file.read()
            except FileNotFoundError:
                return 'Справка не найдена.'

    class AboutDialog(QDialog):
        def __init__(self):
            super().__init__()
            self.setWindowTitle('О приложении')

            text_browser = QTextBrowser()
            text_browser.setPlainText(self.load_about_text())
            text_browser.setReadOnly(True)

            layout = QVBoxLayout(self)
            layout.addWidget(text_browser)

        def load_about_text(self):
            try:
                with open('about.txt', 'r', encoding='utf-8') as file:
                    return file.read()
            except FileNotFoundError:
                return 'Информация о приложении не найдена.'


