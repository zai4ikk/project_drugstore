from PyQt6.QtWidgets import (QWidget, QScrollArea, QVBoxLayout, QFormLayout, QLabel, QComboBox,
                             QPushButton, QSpinBox, QMessageBox, QLineEdit)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import mysql.connector
import sys

class ClientMedicationList(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Список медикаментов")

        self.layout = QVBoxLayout()

        # Добавление выпадающего списка для выбора группы медикаментов
        self.group_combobox = QComboBox(self)
        self.group_combobox.addItem("Все группы")  # Первый элемент для показа всех медикаментов

        # Подключение к базе данных
        try:
            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="sas",
                database="pharmacy"
            )
            print("Подключение к базе данных успешно.")
        except mysql.connector.Error as err:
            print(f"Ошибка подключения к базе данных: {err}")
            QMessageBox.critical(self, "Ошибка", f"Ошибка подключения к базе данных: {err}")
            sys.exit(1)

        self.populate_group_combobox()  # Заполнение выпадающего списка данными из базы данных
        self.group_combobox.currentIndexChanged.connect(self.update_medication_list)

        # Добавление выпадающего списка в основной макет
        self.layout.addWidget(self.group_combobox)

        # Создание области прокрутки для отображения информации о медикаментах
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Создание виджета для размещения макета информации о медикаментах
        content_widget = QWidget()
        self.scroll_layout = QFormLayout(content_widget)

        # Добавление content_widget в область прокрутки
        scroll_area.setWidget(content_widget)

        # Добавление области прокрутки в основной макет
        self.layout.addWidget(scroll_area)

        # Кнопка для просмотра корзины
        self.view_cart_button = QPushButton("Просмотр корзины", self)
        self.view_cart_button.clicked.connect(self.view_cart)
        self.layout.addWidget(self.view_cart_button)

        # Инициализация корзины
        self.cart = []

        # Вызов функции обновления списка медикаментов при инициализации
        self.update_medication_list()

        self.setLayout(self.layout)

    def populate_group_combobox(self):
        # Запрос к базе данных для получения списка групп медикаментов
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT DISTINCT Groupmedicament FROM Assignationmedicament")
            groups = cursor.fetchall()

            # Добавление групп в выпадающий список
            for group in groups:
                self.group_combobox.addItem(group[0])
            print("Группы медикаментов успешно загружены.")
        except mysql.connector.Error as err:
            print(f"Ошибка запроса к базе данных: {err}")
            QMessageBox.critical(self, "Ошибка", f"Ошибка запроса к базе данных: {err}")

    def update_medication_list(self):
        # Получение выбранной группы медикаментов
        selected_group = self.group_combobox.currentText()
        print(f"Выбранная группа: {selected_group}")

        # Обновление списка медикаментов в соответствии с выбранной группой
        try:
            cursor = self.db.cursor()

            if selected_group == "Все группы":
                query = """
                    SELECT Medicament.id, Medicament.Name, Medicament.Pricepurchase, Medicament.Pricerealization, 
                    Assignationmedicament.Groupmedicament, Assignationmedicament.Description, Assignationmedicament.Image, 
                    Diseases.Illness 
                    FROM Medicament 
                    INNER JOIN Assignationmedicament ON Medicament.IDAssignationmedicament = Assignationmedicament.id 
                    LEFT JOIN Diseases ON Medicament.IDAssignationmedicament = Diseases.IDAssignationmedicament
                """
                cursor.execute(query)
            else:
                query = """
                    SELECT Medicament.id, Medicament.Name, Medicament.Pricepurchase, Medicament.Pricerealization, 
                    Assignationmedicament.Groupmedicament, Assignationmedicament.Description, Assignationmedicament.Image, 
                    Diseases.Illness 
                    FROM Medicament 
                    INNER JOIN Assignationmedicament ON Medicament.IDAssignationmedicament = Assignationmedicament.id 
                    LEFT JOIN Diseases ON Medicament.IDAssignationmedicament = Diseases.IDAssignationmedicament
                    WHERE Assignationmedicament.Groupmedicament = %s
                """
                cursor.execute(query, (selected_group,))

            medications = cursor.fetchall()

            # Очистка списка виджетов перед обновлением
            for i in reversed(range(self.scroll_layout.rowCount())):
                self.scroll_layout.removeRow(i)

            # Отображение данных
            for medication in medications:
                medication_info = f"""
                    Наименование: {medication[1]}
                    Группа медикаментов: {medication[4]}
                    Описание: {medication[5]}
                    Заболевание: {medication[7]}
                """

                # Создание QLabel для отображения информации о медикаменте
                medication_label = QLabel(medication_info)
                medication_label.setWordWrap(True)

                # Создание QLabel для отображения цены и количества
                price_label = QLabel(f"Цена: {medication[3]} руб.")
                quantity_spinbox = QSpinBox()
                quantity_spinbox.setMinimum(1)
                quantity_spinbox.setMaximum(100)

                # Создание кнопки для добавления в корзину
                add_to_cart_button = QPushButton("Добавить в корзину", self)
                add_to_cart_button.clicked.connect(lambda _, med=medication, qty=quantity_spinbox: self.add_to_cart(med, qty))

                # Получение пути к изображению из базы данных
                image_path = medication[6]

                # Создание QLabel для отображения изображения
                image_label = QLabel()
                pixmap = QPixmap(image_path)
                image_label.setPixmap(pixmap)
                image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

                # Добавление метки медикамента, метки изображения, цены и кнопки в макет
                self.scroll_layout.addRow(medication_label, image_label)
                self.scroll_layout.addRow(price_label, quantity_spinbox)
                self.scroll_layout.addRow(add_to_cart_button)
            print("Список медикаментов успешно обновлен.")
        except mysql.connector.Error as err:
            print(f"Ошибка запроса к базе данных: {err}")
            QMessageBox.critical(self, "Ошибка", f"Ошибка запроса к базе данных: {err}")

    def add_to_cart(self, medication, quantity_spinbox):
        medication_id = medication[0]
        medication_name = medication[1]
        price = medication[3]
        quantity = quantity_spinbox.value()

        # Добавление медикамента в корзину
        self.cart.append((medication_id, medication_name, price, quantity))

        # Показ сообщения о добавлении в корзину
        QMessageBox.information(self, "Корзина", f"{medication_name} добавлен в корзину в количестве {quantity}.")

    def view_cart(self):
        cart_info = "Корзина:\n"
        total_price = 0
        for item in self.cart:
            cart_info += f"{item[1]} - {item[3]} шт. по {item[2]} руб.\n"
            total_price += item[2] * item[3]
        cart_info += f"Общая стоимость: {total_price} руб."

        # Показ информации о корзине
        QMessageBox.information(self, "Корзина", cart_info)

        # Показ диалогового окна для подтверждения заказа
        reply = QMessageBox.question(self, "Оформить заказ", "Вы хотите оформить заказ?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.place_order()

    def place_order(self):
        # Окно для ввода информации о клиенте и получателе
        client_info_dialog = QWidget()
        client_info_layout = QVBoxLayout()

        self.client_name_input = QLineEdit()
        self.client_name_input.setPlaceholderText("Введите имя сотрудника")
        client_info_layout.addWidget(self.client_name_input)

        self.employee_name_input = QLineEdit()
        self.employee_name_input.setPlaceholderText("Введите имя администратора сервиса")
        client_info_layout.addWidget(self.employee_name_input)

        self.recipient_input = QLineEdit()
        self.recipient_input.setPlaceholderText("Введите название получателя")
        client_info_layout.addWidget(self.recipient_input)

        self.recipient_address_input = QLineEdit()
        self.recipient_address_input.setPlaceholderText("Введите адрес получателя")
        client_info_layout.addWidget(self.recipient_address_input)

        submit_button = QPushButton("Подтвердить")
        submit_button.clicked.connect(lambda: self.confirm_order(client_info_dialog))
        client_info_layout.addWidget(submit_button)

        client_info_dialog.setLayout(client_info_layout)
        client_info_dialog.setWindowTitle("Информация о заказе")
        client_info_dialog.show()

    def confirm_order(self, dialog):
        client_name = self.client_name_input.text()
        employee_name = self.employee_name_input.text()
        recipient = self.recipient_input.text()
        recipient_address = self.recipient_address_input.text()

        if not client_name or not employee_name or not recipient or not recipient_address:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return

        try:
            cursor = self.db.cursor()

            # Получение ID клиента
            cursor.execute("SELECT id FROM client WHERE Name = %s", (client_name,))
            client_id = cursor.fetchone()
            if not client_id:
                QMessageBox.warning(self, "Ошибка", "Сотрудник не найден.")
                return
            client_id = client_id[0]

            # Получение ID сотрудника
            cursor.execute("SELECT id FROM employee WHERE FullName = %s", (employee_name,))
            employee_id = cursor.fetchone()
            if not employee_id:
                QMessageBox.warning(self, "Ошибка", "Администратор не найден.")
                return
            employee_id = employee_id[0]

            # Вставка заказа в таблицу orders
            delivery_cost = 100.0  # Примерная стоимость доставки
            cursor.execute("""
                INSERT INTO orders (IDClient, IDEmployee, Dateofplacement, Deliverycost, Recipient, Recipientaddress) 
                VALUES (%s, %s, CURDATE(), %s, %s, %s)
            """, (client_id, employee_id, delivery_cost, recipient, recipient_address))
            order_id = cursor.lastrowid

            # Вставка медикаментов в таблицу ordered
            for item in self.cart:
                medication_id, _, price, quantity = item
                cursor.execute("""
                    INSERT INTO ordered (IDMedicament, Pricerealization, Quantity, IDOrders)
                    VALUES (%s, %s, %s, %s)
                """, (medication_id, price, quantity, order_id))

            self.db.commit()
            print("Order placed successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.db.rollback()
            QMessageBox.warning(self, "Ошибка", f"Не удалось оформить заказ: {err}")
            return

        # Очистка корзины
        self.cart.clear()

        # Закрытие диалогового окна
        dialog.close()

        # Показ сообщения об успешном оформлении заказа
        QMessageBox.information(self, "Заказ", "Ваш заказ успешно оформлен.")
