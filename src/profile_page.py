import sys
from uuid import uuid4

from PIL import Image
from PyQt5.QtWidgets import QWidget, QFileDialog

from . import db_help
from .about_user import InfoPage
from .statistic import StatisticPage
from ui.ui_profile import Ui_Form


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


class ProfilePage(QWidget, Ui_Form):
    """Вкладка 'Профиль'"""

    def __init__(self, person_id,
                 connection):  # Инициализация id
        # пользователя и соединения с БД
        self.connection = connection
        self.person_id = person_id
        self.ok_draw = False  # Флажок нужен для
        # обновления Профиля в определённый момент
        super().__init__()
        self.setupUi(self)
        self.initUi()

    def initUi(self):
        """Инициализация нужного интерфейса"""

        # Установка в label имени, полученного запросом из БД
        self.name_label.setText(
            db_help.get_name(self.connection, self.person_id))

        # Подготовка файл для записи изображения пользователя
        # Получение поток байтов изображения пользователя из БД
        image = db_help.get_picture(self.connection, self.person_id)
        if image:
            self.btn_image.setText('')
            # Установка полученного файла на кнопку в качестве фото Профиля
            self.btn_image.setStyleSheet(
                f"border-image: url('img/users/{image}')")

        # Подключение кнопок (статистика, информация, смена фото профиля)
        self.btn_info.clicked.connect(self.open_info_page)
        self.btn_statistic.clicked.connect(self.open_statistic_page)
        self.btn_image.clicked.connect(self.set_photo)

    def paintEvent(self, a0) -> None:
        """Перерисовка вкладки 'Профиль'"""

        if self.ok_draw:
            # Обновление имя пользователя в label
            self.name_label.setText(
                db_help.get_name(self.connection, self.person_id))

            # Получаю свежую скорость и точность из БД
            speed, accuracy = db_help.get_max_speed_accuracy(self.connection,
                                                             self.person_id)

            # Обновление скорости и точности пользователя в label'ах
            self.speed_label.setText(f"{speed} зн/мин")
            self.accuracy_label.setText(f"{accuracy} %")

            # Отключаю флаг для рисования
            self.ok_draw = False

    def set_photo(self):
        """Установка фото профиля"""

        name, extensions = QFileDialog.getOpenFileName(self, 'Выберите фото',
                                                       '', 'Картинка (*.png)')
        if name:
            picture_name = f'{uuid4().hex}.png'
            image = Image.open(name)
            image = image.resize((190, 190))
            image.save(f'img/users/{picture_name}')
            self.btn_image.setText('')
            # Установка фото на кнопку
            self.btn_image.setStyleSheet(
                f"border-image: url('img/users/{picture_name}')")
            db_help.set_picture(self.connection,
                                self.person_id, picture_name)  # Обновление фото в самое БД

    def open_info_page(self):
        """Открытие окна информации о польователе"""

        # Создание окна информации, в init передаётся id пользователя,
        # вкладка Профиль и соединение с БД
        self.info_page = InfoPage(self.person_id, self, self.connection)
        self.info_page.show()

    def open_statistic_page(self):
        """Открытие окна статистики пользователя"""

        # Создание окна статистики, в init
        # передаётся id пользователя и соединение с БД
        self.statistic_page = StatisticPage(self.person_id, self.connection)
        self.statistic_page.show()

    def refresh_profile(self):
        """Обновление вкладки Профиль"""
        self.ok_draw = True  # Разрешение на перерисовку
        self.repaint()
