import sys

from PyQt5.QtWidgets import QDialog

import db_help
from ui_registration_dialog import Ui_Dialog


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


class RegistrationForm(QDialog, Ui_Dialog):
    """Форма регистрации"""

    def __init__(self, enter_page, connection):
        # инициализация enter_page (приветственное окно), как родителя,
        # чтобы после открыть его и соединения с БД
        super().__init__()
        self.enter_page = enter_page
        self.connection = connection
        self.setupUi(self)
        self.initUi()

    def initUi(self):
        """Инциализация нужного интерфейса"""

        self.wrong_name.hide()
        self.wrong_email.hide()

    def accept(self):
        """Подтерждение (нажата кнопка OK)"""

        if_wrong, name = False, self.name_line.text()

        # Скрываю Label'ы о том, что данные некорректны
        self.wrong_name.hide()
        self.wrong_email.hide()

        # Генерация пароля юзера, чтобы отправить на почту
        email, password = self.email_line.text(), db_help.generate_password(8)

        # Проверка имени на корректность
        if not name.isalpha():
            self.wrong_name.show()
            return

        # Регистрация аккаунта (если возвращает
        # 'exist' или 'wrong' - значит почта неверная)
        check_email = self.register_account(name, email, password)

        # Если почта некорректна, сообщаем
        # пользователю об ошибке (показываем label)
        if check_email == 'wrong':
            self.wrong_email.setText(
                'Неверный логин! Логин должен состоять из букв и цифр')
            self.wrong_email.show()
            return

        # Если почта уже существует, сообщаем
        # пользователю об ошибке (показываем label)
        elif check_email == 'exist':
            self.wrong_email.setText('Такой логин уже есть')
            self.wrong_email.show()
            return

        super().accept()

    def register_account(self, name, email, password):
        """Регистрация пользователя"""

        # Если такая почта уже есть, то возвращается код возврата 'exist'
        if email in db_help.get_users_data(self.connection):
            return 'exist'

        # Если со стороны сервера почты возвращается
        # True, значит почта некорректна
        if not email.isalnum() or email.isdigit() or email.isalpha():
            return 'wrong'

        with open('ПАРОЛЬ.txt', mode='w') as pass_file:
            pass_file.write(
                'Ваш логин: ' + email + '\nВаш пароль: ' + password +
                '\n\nОбязательно запишите пароль. Он будет стёрт.')

        # Отправка данных в БД, чтобы зарегистрировать пользователя
        db_help.register(self.connection, email, name, password)
