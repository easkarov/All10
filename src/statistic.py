import sys
from datetime import datetime

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QHeaderView

from . import db_help
from ui.ui_statistic import Ui_Form


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


sys.excepthook = except_hook


class StatisticPage(QWidget, Ui_Form):
    """Окно статистики пользователя"""

    # Инициализация id пользователя и соединения с БД
    def __init__(self, person_id, connection):
        super().__init__()
        self.connection = connection
        self.person_id = person_id
        self.mode = -1  # Режим отображения (таблица или граф)
        self.setupUi(self)
        self.initUi()

    def initUi(self):
        """Инициализация интерфейса"""

        # Первоначально открыта таблица, а график скрыт
        self.profile_graph.hide()
        self.profile_table.setSortingEnabled(
            True)  # Установка сортировки по столбцу

        # Подключение сигналов к двум группам кнопок (radio)
        self.table_graph.buttonToggled.connect(
            self.table_or_graph)  # Таблица или график
        self.mode_of_sorting.buttonToggled.connect(
            self.make_statistic)  # Фильтр сортировки

        # Построение статистики в таблице
        self.make_statistic(
            self.btn_today)  # По умолчанию строится за сегодняшний день

    def table_or_graph(self, button):
        # Если кнопка нажата
        if button.isChecked():
            radio_btn_text = button.text()  # Считывание текста нажатой кнопки

            # Если "График", скрытие таблицы и построение
            # графика, если "Таблица" - наоборот
            if radio_btn_text == 'Таблица':
                self.profile_graph.hide()
                self.profile_table.show()
            elif radio_btn_text == 'График':
                self.profile_table.hide()
                self.profile_graph.show()
            self.mode *= -1  # Смена режима отображения
            self.btn_today.setChecked(
                True)  # По умолчанию стоит фильтр сортировки "Сегодня"
            self.make_statistic(
                self.btn_today)  # Построение статистики за "Сегодня"

    def make_statistic(self, button):
        """Построение статистики"""

        if button.isChecked():  # Если кнопка нажата
            radio_btn_text = button.text()  # Считывание текста нажатой кнопки
            self.profile_table.setSortingEnabled(
                False)  # Установка сортировки по столбцу

            # Получение всех попыток пользователя за выбранный период из БД
            attempts = db_help.get_attempts(self.connection, radio_btn_text,
                                            self.person_id)

            if self.mode == -1:  # Если выбрана таблица
                # Установка параметров таблицы
                self.profile_table.setColumnCount(3)
                self.profile_table.setHorizontalHeaderLabels(
                    ('Скорость, зн/мин', 'Точность, %', 'Дата'))
                self.profile_table.setRowCount(0)

                # Заполнение таблицы
                for i, row in enumerate(sorted(attempts)):
                    self.profile_table.setRowCount(
                        self.profile_table.rowCount() + 1)
                    # Считываниие скорости, точности, дня, месяца и года попытки
                    speed, accuracy, day, month, year, hour, minute = row

                    # Преобразование даты именно в такой вид, потому что
                    # QTableWidget считает это датой
                    data = datetime(year, month, day, hour, minute).strftime(
                        '%y-%m-%d %H:%M')

                    # Установка значений
                    self.profile_table.setItem(i, 0,
                                               QTableWidgetItem(str(speed)))
                    self.profile_table.setItem(i, 1,
                                               QTableWidgetItem(str(accuracy)))
                    self.profile_table.setItem(i, 2, QTableWidgetItem(data))
                    # Установка размера шрифта
                    self.profile_table.item(i, 0).setFont(QFont("Days", 16))
                    self.profile_table.item(i, 1).setFont(QFont("Days", 16))
                    self.profile_table.item(i, 2).setFont(QFont("Days", 16))

                # Преобразование таблицы в красивый вид
                self.profile_table.resizeColumnsToContents()
                self.profile_table.resizeRowsToContents()
                a = QHeaderView.Stretch
                self.profile_table.horizontalHeader().setSectionResizeMode(1, a)
                self.profile_table.setSortingEnabled(
                    True)  # Установка сортировки по столбцу

            else:  # Если выбран график
                # Чистка графика
                self.profile_graph.clear()

                # Если выбран фильтр "Сегодня"
                if radio_btn_text == 'Сегодня':
                    # Построение графика по кол-ву попыток
                    # и их скорости за сегодняшний день
                    self.profile_graph.plot(range(1, len(attempts) + 1),
                                            [i[0] for i in attempts])

                elif radio_btn_text == 'За месяц':  # Если выбран
                    # фильтр "За месяц"
                    # Создание словаря с значениями по
                    # умолчанию (ключи - числа от 1 до 31)
                    days = dict.fromkeys(range(1, 32), 0)

                    for day in range(1, 32):  # day в роли дня месяца
                        # Поиск нужных попыток по фильтру
                        speeds = [int(i[0]) for i in attempts if i[2] == day]
                        if speeds:  # Если такие попытки имеются
                            # Записываем в словарь среднюю скорость за этот день
                            days[day] = sum(speeds) // len(speeds)

                    # Построение графика по дням месяца
                    # и средней скорости за эти дни
                    self.profile_graph.plot(list(days.keys()),
                                            list(days.values()))

                elif radio_btn_text == 'За год':  # Если выбран фильтр "За год"
                    # Создание словаря с значениями
                    # по умолчанию (ключи - числа от 1 до 13)
                    monthes = dict.fromkeys(range(1, 13), 0)

                    for month in range(1, 13):  # month в роли месяца года
                        # Поиск нужных попыток по фильтру
                        speeds = [int(i[0]) for i in attempts if i[3] == month]
                        if speeds:  # Если таковые имеются
                            # Записываем в словарь
                            # среднюю скорость за этот месяц
                            monthes[month] = sum(speeds) // len(speeds)

                    # Построение графика по месяцам шлжа
                    # и средней скорости за эти месяцы
                    self.profile_graph.plot(list(monthes.keys()),
                                            list(monthes.values()))
