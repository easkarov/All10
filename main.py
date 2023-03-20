import sqlite3
import sys

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication

from src.enter_page import EnterPage


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    program = QApplication(sys.argv)
    program.setStyleSheet('QWidget {color: white; font-family: "Days";}')
    program.setWindowIcon(QIcon('img/icon.ico'))
    # Созадие объекта соединение в блоке with, чтобы после
    # завершения программы, соединение закрылось
    with sqlite3.connect('db/all10.db') as connection:
        # Передача в init окна объекта соединения
        enter_window = EnterPage(connection)
        enter_window.showMaximized()
        sys.excepthook = except_hook
        sys.exit(program.exec())
