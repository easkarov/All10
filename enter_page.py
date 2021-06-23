import sqlite3
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget

from registration import RegistrationForm
from sign_in import SignInForm
from ui_enter_page import Ui_Form


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


class EnterPage(QWidget, Ui_Form):
    """Приветственное окно (войти, регистрация, выйти)"""

    # Инциализация соединения с БД
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.setupUi(self)
        self.initUi()

    def initUi(self):
        """Инициализация нужного интерфейса"""

        self.verticalLayout.setAlignment(Qt.AlignVCenter)

        self.btn_sign_up.clicked.connect(self.sign_up)
        self.btn_sign_in.clicked.connect(self.sign_in)
        self.btn_exit.clicked.connect(self.close)

    def sign_up(self):
        """Создание формы регистрации"""

        # В init формы регистрации передаю приветственное
        # окно (self) и соединение с БД
        self.reg_dialog = RegistrationForm(self, self.connection)
        self.reg_dialog.show()

    def sign_in(self):
        """Создание формы входа"""

        # В init формы входа передаю приветственное
        # окно (self) и соединение с БД
        self.sign_in_form = SignInForm(self, self.connection)
        self.sign_in_form.show()


if __name__ == '__main__':
    program = QApplication(sys.argv)
    program.setStyleSheet('QWidget {color: white; font-family: "Days";}')
    program.setWindowIcon(QIcon('Изображения/icon.ico'))
    # Созадие объекта соединение в блоке with, чтобы после
    # завершения программы, соединение закрылось
    with sqlite3.connect('all10.db') as connection:
        # Передача в init окна объекта соединения
        enter_window = EnterPage(connection)
        enter_window.showMaximized()
        sys.excepthook = except_hook
        sys.exit(program.exec())
