from PyQt6.QtWidgets import QWidget, QScrollArea, QVBoxLayout, QLabel, QPushButton, QMainWindow
import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from openpyxl import Workbook


class ReportWindow(QMainWindow):
    def __init__(self, data):
        super().__init__()

        self.setWindowTitle("Диаграмма поставок медикаментов")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Преобразование данных в формат, удобный для построения графика
        providers = [item[0] for item in data]
        prices = [item[5] for item in data]

        # Создание горизонтальной столбчатой диаграммы
        fig, ax = plt.subplots()
        ax.barh(providers, prices)
        ax.set_xlabel('Цена закупки')
        ax.set_ylabel('Поставщик')
        ax.set_title('Диаграмма поставок медикаментов')

        # Создание холста для графика
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)


class ProviderList(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Список поставщиков")

        self.layout = QVBoxLayout()

        # Кнопки
        medication_button = QPushButton("Диаграмма поставок медикаментов")
        providers_button = QPushButton("Отчет о поставках")

        # Добавление кнопок в компоновку
        self.layout.addWidget(medication_button)
        self.layout.addWidget(providers_button)

        # Создание области прокрутки для отображения информации о поставщиках
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Создание виджета для размещения компоновки с информацией о поставщиках
        content_widget = QWidget()
        scroll_layout = QVBoxLayout(content_widget)

        # Добавление виджета content_widget в область прокрутки
        scroll_area.setWidget(content_widget)

        # Добавление области прокрутки в основную компоновку
        self.layout.addWidget(scroll_area)

        # Подключение к базе данных
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="sas",
            database="pharmacy"
        )

        cursor = db.cursor()

        # Получение данных из таблицы Provider и Medicament
        cursor.execute(
            "SELECT Provider.Name, Provider.Representative, Provider.Post, "
            "Medicament.Name AS MedicamentName, Medicament.Unitsofmeasurement, Medicament.Pricepurchase "
            "FROM Provider LEFT JOIN Medicament ON Provider.id = Medicament.IDProvider"
        )
        providers = cursor.fetchall()

        # Отображение данных
        self.report_data = providers
        for provider in providers:
            provider_info = f"""
                Наименование поставщика: {provider[0]}
                Представитель: {provider[1]}
                Должность: {provider[2]}
                Медикамент: {provider[3]}
                Единицы измерения: {provider[4]}
                Цена закупки: {provider[5]}
            """

            # Создание QLabel для отображения информации о поставщике
            provider_label = QLabel(provider_info)

            # Установка автопереноса слов для QLabel
            provider_label.setWordWrap(True)

            # Добавление QLabel с информацией о поставщике в компоновку прокрутки
            scroll_layout.addWidget(provider_label)

        # Подключение события нажатия кнопки к методам show_report и show_providers
        medication_button.clicked.connect(self.show_report)
        providers_button.clicked.connect(self.show_providers)

        # Создание переменной экземпляра report_window для ее сохранения
        self.report_window = None

        self.setLayout(self.layout)

    def show_report(self):
        # Создание и отображение окна с отчетом
        self.report_window = ReportWindow(self.report_data)
        self.report_window.show()

    def show_providers(self):
        # Создание и сохранение отчета в формате Excel
        wb = Workbook()
        ws = wb.active
        ws.append(["Наименование поставщика", "Представитель", "Должность", "Медикамент", "Единицы измерения", "Цена закупки"])

        for provider in self.report_data:
            ws.append([provider[0], provider[1], provider[2], provider[3], provider[4], provider[5]])

        # Сохранение книги
        wb.save('отчет_о_поставках.xlsx')

        # Открытие файла Excel с помощью приложения по умолчанию
        import os
        os.system('start excel отчет_о_поставках.xlsx')

