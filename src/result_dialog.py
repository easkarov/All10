from PyQt5.QtWidgets import QDialog

from ui.ui_result_dialog import Ui_Dialog


class ResultPage(QDialog, Ui_Dialog):
    """Окно результата тестирования"""

    # Инициализация окна тестирования (родитель), скорости и точности
    def __init__(self, testing_page, speed, accuracy):
        super().__init__()
        self.testing_page = testing_page
        self.speed = speed
        self.accuracy = accuracy
        self.setupUi(self)
        self.initUi()

    def initUi(self):
        """Инициализация интерфейса"""

        # Установка скорости и точности в label'ы
        self.speed_label.setText(f"{int(self.speed)} зн/мин")
        self.accuracy_label.setText(f"{self.accuracy}%")

    def accept(self):
        """Подтверждение (нажатие кнопки ОК)"""

        self.testing_page.start_again()  # Начать тестирование заново
        super().accept()

    def reject(self):
        """Нажатие кнопки NO"""

        self.testing_page.close()  # Закрытие окна тестирования
        super().reject()
