from PyQt5.QtWidgets import QWidget

from . import db_help
from ui.ui_about_user import Ui_Form


def check_password(password):
    """Проверка пароля на корректность"""

    if not len(password) >= 8:
        return 0
    elif password == password.lower() or password == password.upper():
        return 1
    elif not any(map(str.isdigit, password)):
        return 2


class InfoPage(QWidget, Ui_Form):
    """Окно информации о пользователе"""

    # Инициализация id пользователя и вкладки "Профиль" (родитель) и
    # соединения с БД
    def __init__(self, person_id, profile_page, connection):
        super().__init__()
        self.person_id = person_id
        self.profile_page = profile_page
        self.connection = connection
        self.setupUi(self)
        self.initUi()

    def initUi(self):
        """Инициализация интерфейса"""

        # Получение всех данных пользователя из БД по его id
        mail, name, surname = db_help.get_user_data(self.connection,
                                                    self.person_id)

        # Установка этих данных по виджетам (lineEdit)
        self.name_line.setText(name)
        self.surname_line.setText(surname)
        self.login_line.setText(mail)

        # Скрытие текста ошибок некорректных данных
        self.wrong_name.hide()
        self.wrong_surname.hide()
        self.wrong_password.hide()

        self.btn_save_info.clicked.connect(self.save_info)
        self.btn_edit_info.clicked.connect(self.edit_info)

    def edit_info(self):
        """Редактирование информации о пользователе"""

        # Доступ к смене данных
        self.name_line.setReadOnly(False)
        self.surname_line.setReadOnly(False)
        self.password_line.setReadOnly(False)

    def save_info(self):
        """Сохранение данных пользователя"""

        if not self.name_line.isReadOnly():
            # Скрытие текста ошибок
            self.wrong_name.hide()
            self.wrong_surname.hide()
            self.wrong_password.hide()

            if_wrong = False  # Флажок, если какие-то из данных
            # будут некорректными

            # Считывание данных, введённых пользователем
            name = self.name_line.text()
            surname = self.surname_line.text()
            password = self.password_line.text()

            # Проверка имени
            if not name.isalpha():
                if_wrong = True
                self.wrong_name.show()

            # Проверка фамилии
            if surname and not surname.isalpha():
                if_wrong = True
                self.wrong_surname.show()

            # Проверка пароля
            answer = check_password(password) if password else None
            if answer is not None:
                self.wrong_password.show()  # Показ сообщения об ошибке
                # Смена текста ошибки на нужный (в зависимости от кода возврата)
                if answer == 0:
                    self.wrong_password.setText(
                        'Пароль должен быть не менее 8 символов')
                elif answer == 1:
                    self.wrong_password.setText(
                        'Пароль должен содержать строчные и заглавные буквы')
                else:
                    self.wrong_password.setText(
                        'Пароль должен содержать хотя бы одну цифру')
                if_wrong = True  # Смена флажка

            if if_wrong:
                return

            # Обновление данных пользователя на введённые им в БД
            db_help.set_user_data(self.connection, self.person_id, name,
                                  password, surname)

            # Запрет на редактирование данных
            self.name_line.setReadOnly(True)
            self.surname_line.setReadOnly(True)
            self.password_line.setReadOnly(True)

            # Обновление вкладки "Профиль"
            self.profile_page.refresh_profile()
