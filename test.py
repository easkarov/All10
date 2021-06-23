import re
import sys
from time import time

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QShortcut

import db_help
from result_dialog import ResultPage
from ui_test import Ui_Form

# Список используемых символов
SYMBOLS = f"Ё 1 2 3 4 5 6 7 8 9 0 - = Й Ц У К Е Н Г Ш Щ З Х Ъ \\ " \
          f"Ф Ы В А П Р О Л Д Ж Э Я Ч С М И Т Ь Б Ю .".split() + [' ']


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


class TestingPage(QWidget, Ui_Form):
    """Окно тестирования"""

    # Инциализация главного окна (для того чтобы в будущем открыть его),
    # id пользователя и соединение с БД
    def __init__(self, main_window, person_id, connection):
        super().__init__()
        self.setupUi(self)

        self.main_window = main_window  # Инициализация главного окна
        self.person_id = person_id  # Инициализация id пользователя
        self.connection = connection  # Инициализация соединения с БД

        # Установка горячих клавиш Shift + R,
        # который начинают тестирование заново
        QShortcut(QtGui.QKeySequence("Shift+R"), self, self.start_again)

        # Получение из БД рандомного предложения для тестирования
        self.letters = db_help.get_sentence(self.connection)

        self.letters_copy = self.letters.copy()  # Копия букв этого предложения
        self.flag_typing = 0  # Флажок - начало печатания
        self.ind = 0  # Индекс буквы в предложении,
        # на которой сейчас пользователь
        # Все кнопки клавиатуры
        self.buttons_keys = self.group_of_buttons.buttons()
        self.length_lets = len(self.letters)  # Длина предложения

        self.initUi()

    def initUi(self):
        """Инициализация интерфейса"""

        # Покраска самой первой буквы в зелёный
        self.letters[0] = f'<span style=\'background-color: #5bc538; color:' \
                          f'white;\'>{self.letters[0]}</span>'

        # Поиск индекс кнопки с текстом -
        # символом равным символу в тренировочном предложении
        ind_key = SYMBOLS.index(self.letters_copy[0].upper())

        # Установка стиля на кнопку, которую вот-вот должен нажать пользователь
        self.buttons_keys[ind_key].setStyleSheet(
            'border-style: solid; border-width: 3px; border-color: white;')

        # Визуализация стилей в виджете QTextBrowser
        self.sentence.setHtml(
            f"""<p align="center">{''.join(self.letters)}</p>""")

    def keyPressEvent(self, a0: QtGui.QKeyEvent):
        """Обработка нажатий клавиш"""

        # Как только пользователь начал печатать, запустился секундомер
        if not self.flag_typing:
            self.start = time()  # Локальное время
            # начала тестирования (значение будет менятся)
            self.global_start = time()  # Глобальное время начала тестирования
            self.flag_typing = 1  # Поднятие флажка
            self.mistakes = (
            self.length_lets, 0)  # Обнуление кол-ва ошибок тестирования

        # Если нажат Escape, окно теста закрывается
        if a0.key() == Qt.Key_Escape:
            self.close()

        # Проверка на то, что нажата русская буква, которая совпадает
        # с текущим символом в тренировочном предложении, или пробел
        elif (bool(re.search('[а-яА-Яё]', a0.text())) and a0.text() ==
              self.letters_copy[self.ind]) or \
                (a0.key() == Qt.Key_Space and self.letters_copy[
                    self.ind] == ' '):

            # Обнуление флажка счётчика ошибок
            # после верно напечатанного символа,
            # то есть произошло переключение на другой символ
            self.mistakes = (self.mistakes[0], 0)

            # Визуальное обновление скорости на экране после каждых 3 символов
            if not (self.ind + 1) % 3:
                current_time = time()  # Время на момент нажатия клавиши
                self.speed_label.setText(
                    f"{int(3 // ((current_time - self.start) / 60))} зн/мин")
                self.start = current_time  # Обновление локального времени

            # Покраска верно напечатанного символа предложения в зелёный цвет
            self.letters[self.ind] = f'<span style=\'color: #5bc538;\'>' \
                                     f'{self.letters_copy[self.ind]}</span>'

            # Поиск кнопки, соответсвующей данному
            # символу и установка смены цвета, при её нажатии
            current_button = self.buttons_keys[
                SYMBOLS.index(self.letters_copy[self.ind].upper())]
            current_button.setStyleSheet(
                'QPushButton:pressed {background-color:'
                '#5bc538;}')
            # Искуственная эмуляция нажатия кнопки на 100 мс
            current_button.animateClick(100)

            # Проверка на то, что пользователь закончил
            # печать тренировочного предложения
            if self.ind == self.length_lets - 1:
                # Вычисление скорости (зн/мин) кол-во символов предложения
                # // ((время на момент нажатия
                # последней клавиши - глобальное время начала) / 60)
                speed = self.length_lets // ((time() - self.global_start) / 60)

                # Вычисление точности в % (кол-во ошибок / кол-во символов)
                accuracy = round(self.mistakes[0] / self.length_lets * 100, 1)

                # Визуализация стилей в виджете QTextBrowser
                self.sentence.setHtml(
                    f"""<p align="center">{''.join(self.letters)}</p>""")

                # Запись результата в БД (скорость, точность, id)
                db_help.write_result(self.connection, speed, accuracy,
                                     self.person_id)

                # Создание диалогового окна с результатом,
                # передача в init скорости и точности
                self.result_page = ResultPage(self, speed, accuracy)
                self.result_page.show()

                # Пропкуск дальнейших действий
                return

            # Обновление индекса на котором сейчас пользователь
            self.ind += 1

            # Покраска ФОНА символа в зелёный цвет,
            # на который ДОЛЖЕН нажать пользователь
            self.letters[self.ind] = f'<span style=\'background-color:' \
                                     f'#5bc538;' \
                                     f'color: white;' \
                                     f'\'>{self.letters_copy[self.ind]}</span>'

            # Установка белой обводки на кнопку на экране,
            # на которую должен нажать пользователь
            self.buttons_keys[SYMBOLS.index(
                self.letters_copy[self.ind].upper())].setStyleSheet(
                'border-style: solid; border-width: 3px; border-color: white;')

        # Проверка на то что пользователь не нажал спец клавишу и на то
        # что текст клавиши есть в списке доступных символов
        elif a0.text() and a0.text().upper() in SYMBOLS:
            # Если пользователь ошибся на одном
            # и том же месте (символе) первый раз,
            # то счётчик ошибок обновляется
            if self.mistakes[1] == 0:
                self.mistakes = (
                self.mistakes[0] - 1, 1)  # Второе значение в кортеже - флажок

            # Визуальное обновление процента ошибок на экране
            self.accuracy_label.setText(
                f"{self.mistakes[0] / self.length_lets * 100:.1f}%")

            # Поиск кнопку на экране, соответствующую нажатой клавише
            wrong_button = self.buttons_keys[SYMBOLS.index(a0.text().upper())]
            # Установка смены цвета кнопки на красный после нажатия на неё
            wrong_button.setStyleSheet(
                'QPushButton:pressed {background-color: red;}')
            # Искусственная эмуляция нажатия на кнопку в течение 100 мс
            wrong_button.animateClick(100)

            # Покраска ФОНА символа в красный цвет, т. к. пользователь ошибся
            self.letters[
                self.ind] = f'<span style=\'background-color:' \
                            f'red; color: white;\'>' \
                            f'{self.letters_copy[self.ind]}</span>'

        # Визуализация стилей в виджете QTextBrowser
        self.sentence.setHtml(
            f"<p align=\'center\'>{''.join(self.letters)}</p>")

    def start_again(self):
        """Начать тест сначала"""

        # Стирает все стили с действующей кнопки,
        # на которую должен был нажать пользователь
        self.buttons_keys[
            SYMBOLS.index(self.letters_copy[self.ind].upper())].setStyleSheet(
            '')

        # Обновление всех счётчиков, флагов
        self.letters, self.ind = self.letters_copy.copy(), 0
        self.flag_typing = 0

        # Получение из БД рандомного предложения для тестирования
        self.letters = db_help.get_sentence(self.connection)
        self.letters_copy = self.letters.copy()  # Копия букв этого предложения
        self.length_lets = len(self.letters)  # Длина предложения

        # Обновление скорости и точности на экране
        self.speed_label.setText('0 зн/мин')
        self.accuracy_label.setText('100%')
        self.initUi()

    def close(self):
        """Закрытие окна тестирования"""
        self.main_window.show()  # Открытие Главного окна с вкладками
        super().close()
