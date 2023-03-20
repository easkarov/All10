import sys
from hashlib import pbkdf2_hmac

from PyQt5.QtWidgets import QWidget, QLineEdit

from . import db_help
from .main_window import MainWindow
from .recover_password import RecoverPage
from ui.ui_sign_in import Ui_Form


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


def compare_passwords(password, correct_password, salt) -> bool:
    """Сравнение верного пароля пользователя с введённым"""

    # Получение хеша введённого пароля с солью
    hsh = pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000, 16)

    if hsh != correct_password:  # Если хеши неравны, возвращается True
        return True
    return False


class SignInForm(QWidget, Ui_Form):
    """Форма входа"""

    def __init__(self, enter_page, connection):
        """Инициализация enter_page (приветственное окно), как родителя,
        чтобы после открыть его, и соединения с БД"""

        super().__init__()
        self.enter_page = enter_page  # Инициализирую родителя
        self.mode_of_password = -1  # Режим скрыт или показан пароль
        self.connection = connection  # Инициализация соединения
        self.setupUi(self)
        self.initUi()

    def initUi(self):
        """Инициализация нужного интерфейса"""

        self.password_line.setEchoMode(
            QLineEdit.Password)  # Скрытие пароль звёздочками *
        self.wrong_mail.hide()
        self.wrong_password.hide()
        self.btn_sign_in.clicked.connect(self.sign_in)
        self.forget_password.clicked.connect(self.remember_password)
        self.show_hide_password.clicked.connect(self.show_or_hide_password)

    def sign_in(self):
        """Проверка корректности данных пользователя"""

        email, password = self.email_line.text(), self.password_line.text()

        # Скрываю label'ы о том, что данные неверные
        self.wrong_mail.hide()
        self.wrong_password.hide()

        # Парсинг всех данных пользователей (пароль, почта) по всей БД
        data_of_users = db_help.get_users_data(self.connection)

        # Проверка данных с данными пользователя из БД
        # Если почты нет в БД, сообщаю об ошибке (показываю label)
        if email not in data_of_users:
            self.wrong_mail.show()
            return

        correct_password = data_of_users[email][
            1]  # Хеш верного пароля пользователя
        salt = data_of_users[email][2]  # Соль пароля пользователя

        # Если пароль не совпадает, сообщается об ошибке (показываю label)
        if compare_passwords(password, correct_password, salt):
            self.wrong_password.show()
            return

        self.close()
        self.enter_page.close()  # Закрытие приветственного окна

        # При верности данных пользователя открывается главное окно,
        # которое принимает id юзера, приветственное окно и соединение с БД
        self.main_window = MainWindow(data_of_users[email][0], self.enter_page,
                                      self.connection)
        self.main_window.show()

    def remember_password(self):
        """Открытие формы восстановления пароля"""

        self.recover_page = RecoverPage(self.connection)
        self.recover_page.show()
        self.close()

    def show_or_hide_password(self):
        """Показать / скрыть пароль"""

        if self.mode_of_password == -1:
            self.password_line.setEchoMode(
                QLineEdit.Normal)  # Возвращение нормального режима
        else:
            self.password_line.setEchoMode(
                QLineEdit.Password)  # Скрытие пароль звёздочками *
        self.mode_of_password *= -1
