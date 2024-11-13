'''import unittest
from PyQt6.QtWidgets import QApplication
from employee_list import EmployeeList, AddEmployeeDialog


class TestEmployeeList(unittest.TestCase):
    def setUp(self):
        # Создаем объект приложения для тестирования
        self.app = QApplication([])

    def test_employee_list_creation(self):
        # Тестирование создания объекта EmployeeList
        employee_list = EmployeeList()
        self.assertIsInstance(employee_list, EmployeeList)

    def test_add_employee_dialog(self):
        # Тестирование создания объекта AddEmployeeDialog
        employee_list = EmployeeList()
        add_employee_dialog = AddEmployeeDialog(employee_list)
        self.assertIsInstance(add_employee_dialog, AddEmployeeDialog)

    def tearDown(self):
        # Очистка ресурсов после завершения тестов
        self.app.exit()


if __name__ == '__main__':
    unittest.main()'''

