import sys
from uuid import uuid4

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap, QColor, QFont
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QHeaderView, QLabel

from . import db_help
from ui.ui_rating import Ui_Form


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


class RatingPage(QWidget, Ui_Form):
    """Вкладка 'Рейтинг'"""

    # Инициализация соединения с БД
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.setupUi(self)
        self.initUi()

    def initUi(self):
        """Инициализация интерфейса"""

        # Добавление в ComboBox фильтры для сортировки
        self.mode_of_sorting.addItems(['Сегодня', 'За месяц', 'За год'])
        self.mode_of_sorting.currentTextChanged.connect(self.refresh_rating)

        # Обновление рейтинга для построение таблицы
        self.refresh_rating()

    def refresh_rating(self):
        """Обновление таблицы рейтинга"""

        # Задание параметров QTableWidget
        self.rating_table.setColumnCount(4)
        self.rating_table.setHorizontalHeaderLabels(
            ('Фото', 'Имя', 'Скорость, зн/мин', 'Точность, %'))
        self.rating_table.setRowCount(0)

        # Получение рейтинга всех пользователей по
        # их макс скорости (значения уникальные)
        rating = db_help.make_rating(self.connection,
                                     self.mode_of_sorting.currentIndex())

        # Заполнение таблицы
        for i, row in enumerate(sorted(rating, key=lambda x: -x[2])):
            self.rating_table.setRowCount(self.rating_table.rowCount() + 1)

            # Получение потоков байта изображения,
            # имя пользователя, скорость и точность
            picture, name, speed, accuracy = row

            # Label для установки фото профиля пользователя
            image = QLabel('', self)
            image.setFixedSize(50, 50)

            # Заполенинее одной строчки таблицы
            self.rating_table.setItem(i, 1, QTableWidgetItem(str(name)))
            self.rating_table.setItem(i, 2, QTableWidgetItem(str(speed)))
            self.rating_table.setItem(i, 3, QTableWidgetItem(str(accuracy)))
            # Установка размера шрифта
            self.rating_table.item(i, 1).setFont(QFont("Days", 16))
            self.rating_table.item(i, 2).setFont(QFont("Days", 16))
            self.rating_table.item(i, 3).setFont(QFont("Days", 16))

            # Открытие файла-изображение для записи
            picture = QPixmap(f'img/users/{picture}')
            picture = picture.scaled(QSize(50, 50))  # Смена размеров
            image.setPixmap(picture)  # Установка картинки в label

            self.rating_table.setCellWidget(i, 0, image)  # Добавление label в таблицу

            # Покарска первых трёх рядов в нужный цвет
            self.color_row(0, '#edcd00')
            self.color_row(1, '#c0c0c0')
            self.color_row(2, '#cd7f32')

            self.rating_table.resizeColumnsToContents()
            self.rating_table.resizeRowsToContents()
            # Расстягивание таблицу во всю ширину окна
            a = QHeaderView.Stretch
            self.rating_table.horizontalHeader().setSectionResizeMode(1, a)

    def color_row(self, row, color):
        """Покраска одного ряда"""

        if self.rating_table.rowCount() > row:
            for i in range(1, self.rating_table.columnCount()):
                self.rating_table.item(row, i).setBackground(QColor(color))
