import sys

from PyQt5.QtWidgets import QDialog

import db_help
from ui_recover_password import Ui_Dialog


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

    sys.excepthook = except_hook


class RecoverPage(QDialog, Ui_Dialog):
    """Форма восстановления пароля"""

    # Инициализация соединения с БД
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.setupUi(self)
        self.initUi()

    def initUi(self):
        """Инициализация нужного интерфейса"""

        self.wrong_email.hide()

    def accept(self) -> None:
        """Подтерждение (нажата кнопка OK)"""

        self.wrong_email.hide()  # Скрытие label'а об ошибке
        email = self.email_line.text()  # Почта, введённая пользователем

        # Генерирую для этой почты в БД новый пароль
        # и возвращаю его ('', если email нет в БД)
        password = db_help.recover_password(self.connection, email)

        # Если email существует, то password не должен иметь пустое значение
        if not password:
            self.wrong_email.show()
            return

        with open('ПАРОЛЬ.txt', mode='w') as pass_file:
            pass_file.write(
                'Ваш логин: ' + email + '\nВаш новый пароль: ' + password +
                '\n\nОбязательно запишите пароль. Он будет стёрт.')

        super().accept()
