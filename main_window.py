import sys

from PyQt5.QtWidgets import QMainWindow

from pretest import PretestPage
from profile_page import ProfilePage
from rating import RatingPage
from ui_main_window import Ui_MainWindow


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


class MainWindow(QMainWindow, Ui_MainWindow):
    """Главное окно, управляющее вкладками: Рейтинг, Профиль, Претестирование"""

    def __init__(self, person_id, enter_form, connection):
        # Инициализация id пользователя и
        # enter_page (приветственное окно), как
        # родителя, чтобы после открыть его,
        # и соединения с БД
        super().__init__()
        self.connection = connection
        self.enter_form = enter_form
        self.person_id = person_id
        self.setupUi(self)
        self.initUi()

    def initUi(self):
        """Инициализация нужного интерфейса"""

        # Создание вкладок Профиль, Претест и Рейтинг,
        # которые принимают в init соединение с БД
        self.profile_page = ProfilePage(self.person_id, self.connection)
        # В init Претеста добавляется объект MainWindow (self) и id пользователя
        self.pretest_page = PretestPage(self, self.person_id, self.connection)
        self.rating_page = RatingPage(
            self.connection)  # Принимает только соединение с БД

        self.btn_exit.clicked.connect(self.exit)
        self.btn_profile.clicked.connect(self.open_profile)
        self.btn_pretest.clicked.connect(self.open_pretest)
        self.btn_rating.clicked.connect(self.open_rating)

        # Переключение между вкладками реализовано
        # при помощи VLayout и прятками виджетов
        self.tabs.addWidget(self.profile_page)
        self.tabs.addWidget(self.pretest_page)
        self.tabs.addWidget(self.rating_page)

        self.btn_pretest.setStyleSheet('background-color: #edcd00')
        self.btn_pretest.setEnabled(False)

        # Начальной вкладкой является -
        # Претестирование, поэтому остальные скрываются
        self.profile_page.hide()
        self.rating_page.hide()

    def exit(self):
        """Выход из аккаунта"""

        # При выходе из аккаунта закрывается главное окно и
        # открывается вновь приветственное (EnterPage)
        self.close()
        self.enter_form.show()

    def open_profile(self):
        """Открытие вкладки Профиль"""

        # Установка цвета активной кнопки
        self.btn_profile.setStyleSheet('background-color: #edcd00')
        self.btn_pretest.setStyleSheet('')
        self.btn_rating.setStyleSheet('')

        self.btn_pretest.setEnabled(True)
        self.btn_profile.setEnabled(False)
        self.btn_rating.setEnabled(True)

        # При открытии Профиля закрываются Рейтинг, Претестирование
        self.rating_page.hide()
        self.pretest_page.hide()

        # Обновление Профиля при его открытии
        self.profile_page.refresh_profile()
        self.profile_page.show()

    def open_pretest(self):
        """Открытие вкладки Претестирование"""

        # Установка цвета активной кнопки
        self.btn_pretest.setStyleSheet('background-color: #edcd00')
        self.btn_profile.setStyleSheet('')
        self.btn_rating.setStyleSheet('')

        self.btn_pretest.setEnabled(False)
        self.btn_profile.setEnabled(True)
        self.btn_rating.setEnabled(True)

        # При открытии Претестирования закрываются Профиль, Рейтинг
        self.rating_page.hide()
        self.profile_page.hide()
        self.pretest_page.show()

    def open_rating(self):
        """Открытие вкладки Рейтинг"""

        # Установка цвета активной кнопки
        self.btn_rating.setStyleSheet('background-color: #edcd00')
        self.btn_pretest.setStyleSheet('')
        self.btn_profile.setStyleSheet('')

        self.btn_pretest.setEnabled(True)
        self.btn_profile.setEnabled(True)
        self.btn_rating.setEnabled(False)

        # При открытии Рейтинга закрываются Профиль, Претестирование
        self.pretest_page.hide()
        self.profile_page.hide()

        # Обновление Рейтинга при его открытии
        self.rating_page.refresh_rating()
        self.rating_page.show()
