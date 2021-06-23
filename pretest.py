import sys

from PyQt5.QtWidgets import QWidget

from test import TestingPage
from ui_pretest import Ui_Form


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


class PretestPage(QWidget, Ui_Form):
    """Вкладка 'Претестирования'"""

    # Инициализация главного окна MainWindow (оно ещё понадобится),
    # id пользователя и соединения с БД
    def __init__(self, main_window, person_id, connection):
        super().__init__()
        self.main_window = main_window
        self.person_id = person_id
        self.connection = connection
        self.setupUi(self)
        self.initUi()

    def initUi(self):
        """Инициализация нужного интерфейса"""
        self.btn_make_test.clicked.connect(self.open_testing_page)

    def open_testing_page(self):
        """Открытие окна тестирования"""
        self.main_window.close()  # Сразу закрытие MainWindow

        # Создание окна тестирования, передача в init главного окна,
        # id пользователя и соединения с БД
        self.testing_page = TestingPage(self.main_window, self.person_id,
                                        self.connection)
        # Открытие тестирования на весь экран
        self.testing_page.showFullScreen()
