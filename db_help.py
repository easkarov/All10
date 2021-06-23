import sqlite3
import sys
from datetime import datetime
from hashlib import pbkdf2_hmac
from os import urandom
from random import sample
from string import ascii_letters, digits


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


sys.excepthook = except_hook

# Подготовка списка для генерации паролей
SYMBOLS = ascii_letters + digits
for i in 'IloO01':  # Похожие друг на друга символы удаляются
    SYMBOLS.replace(i, '')


def hash_password(password) -> tuple:
    """Хеширование пароля"""

    salt = urandom(16)  # Генерация соли (16 бит)
    # Хеширование пароля (16 бит) функцией sha256 с солью salt
    hsh = pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000, 16)
    return hsh, salt


def generate_password(m) -> str:
    """Генерация пароля"""

    pas = ''.join(sample(SYMBOLS, k=m))
    # Он должен состоять из маленьких и больших
    # букв и содержать хотя бы одну цифру
    while pas.islower() or pas.isupper() or pas.isdigit() or not any(
            map(str.isdigit, pas)):
        pas = ''.join(sample(SYMBOLS, k=m))
    return pas


def register(connection, email, name, password) -> None:
    """Регистрация нового пользователя в БД"""

    hsh, salt = hash_password(password)  # Получение хеша пароля и его соли
    # Добавляем в БД запись (mail, name, password)
    connection.cursor().execute(
        'INSERT INTO about_user(mail, name, hash, salt) VALUES(?, ?, ?, ?)',
        (email, name, hsh, salt))
    connection.commit()


def set_user_data(connection, person_id, name, password, surname=None):
    """Обновление данных пользователя (имя, фамилия, пароль) в БД"""

    if password:
        hsh, salt = hash_password(password)  # Получение хеша пароля и его соли
        connection.cursor().execute(
            'UPDATE about_user SET name = ?, surname = ?, hash = ?, salt = ? '
            'WHERE person_id = ?', (name, surname, hsh, salt, person_id))
    else:
        connection.cursor().execute(
            'UPDATE about_user SET name = ?, surname = ? '
            'WHERE person_id = ?', (name, surname, person_id))
    connection.commit()


def get_user_data(connection, person_id):
    """Получение данных пользователя по его id из БД"""

    return connection.cursor().execute(
        f'''SELECT mail, name, surname FROM about_user
                            WHERE person_id = {person_id}''').fetchone()


def get_users_data(connection) -> dict:
    """Получение данных всех пользователей из БД"""

    # Возвращается словарь (ключи - почты,
    # значения - (id пользователя, хеш, соль))
    return {mail: (person_id, hsh, salt) for person_id, mail, hsh, salt in
            connection.cursor().execute(
                'SELECT person_id, mail, hash, salt FROM about_user')}


def get_name(connection, person_id) -> str:
    """Получениие имени пользователя по его id из БД"""

    return connection.cursor().execute(f'''SELECT name FROM about_user WHERE
                          person_id = {person_id}''').fetchone()[0]


def get_picture(connection, person_id):
    """Получение изображения (поток байт) пользователя из БД"""

    return connection.cursor().execute(f'''SELECT picture FROM about_user
                          WHERE person_id = {person_id}''').fetchone()[0]


def set_picture(connection, person_id) -> None:
    """Установка изображения (поток байт) пользователя в БД"""

    # Открытие файла для чтения изображения
    with open('Изображения/user_image.png', mode='rb') as f:
        image = sqlite3.Binary(f.read())  # Считывание потока байт изображения
        connection.cursor().execute(
            'UPDATE about_user SET picture = ? WHERE person_id = ?',
            (image, person_id))
        connection.commit()


def get_sentence(connection) -> list:
    """Получение рандомного тренировочного предложения из БД"""

    # Использование оператора "RANDOM" и "LIMIT 1"
    sentence = connection.cursor().execute(
        'SELECT sentence FROM sentences ORDER BY RANDOM()'
        'LIMIT 1').fetchone()
    return list(sentence[0])


def write_result(connection, speed, accuracy, person_id) -> None:
    """Запись результата пользователя после прохождения теста в БД по id"""

    current_data = datetime.today()  # Сегодняшняя дата
    connection.cursor().execute('''INSERT INTO attempts(person_id, speed,
                    accuracy, day, month, year, hour, minute)
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?)''',
                                (person_id, speed, accuracy, current_data.day,
                                 current_data.month,
                                 current_data.year, current_data.hour,
                                 current_data.minute))
    connection.commit()


def recover_password(connection, email):
    """Обновление пароля пользователя на сгенерированный по id"""

    # Проверка, что почта пользователя зарегистрирована
    if (email,) in connection.cursor().execute(
            'SELECT mail FROM about_user').fetchall():
        password = generate_password(8)  # Генерация 8-символьного пароля
        hsh, salt = hash_password(password)  # Хеширование нового пароля

        connection.cursor().execute(
            'UPDATE about_user SET hash = ?, salt = ? WHERE mail = ?',
            (hsh, salt, email))
        connection.commit()
        return password
    return ''


def make_rating(connection, mode_of_sorting):
    """Получение рейтинга по всем пользователям"""

    cur_date = datetime.today()  # Сегодняшняя дата

    # Проверка на код возврата (режим сортировки)
    if mode_of_sorting == 0:  # Сортировка по дню
        mode = f'AND day = {cur_date.day} AND month = {cur_date.month} ' \
               f'AND year = {cur_date.year}'
    elif mode_of_sorting == 1:  # Сортировка по месяцу
        mode = f'AND month = {cur_date.month} AND year = {cur_date.year} '
    elif mode_of_sorting == 2:  # Сортировка по году
        mode = f'AND year = {cur_date.year}'

    # Запрос для БД
    for person_id, name, picture in connection.cursor().execute("""SELECT 
    person_id, name, picture FROM about_user""").fetchall():
        speed, accuracy = connection.cursor().execute("""SELECT MAX(speed), 
        accuracy FROM attempts WHERE person_id = ? """ + mode, (person_id,
                                                                )).fetchone()

        # Если пользователь ни разу не проходил тест,
        # то его скорость и точность равны 0
        speed = 0 if speed is None else speed
        accuracy = 0 if accuracy is None else accuracy

        yield picture, name, speed, accuracy  # Возвращается итератор


def get_attempts(connection, mode_of_sorting, person_id):
    """Получение всех попыток пользователя по id"""

    cur_date = datetime.today()  # Сегодняшняя дата

    # Выбор режима сортировки
    if mode_of_sorting == 'Сегодня':
        mode = f'AND day = {cur_date.day} AND month = {cur_date.month} ' \
               f'AND year = {cur_date.year}'
    elif mode_of_sorting == 'За месяц':
        mode = f'AND month = {cur_date.month} AND year = {cur_date.year}'
    elif mode_of_sorting == 'За год':
        mode = f'AND year = {cur_date.year}'

    # Элементарный запрос для БД
    attempts = connection.cursor().execute("""SELECT speed, accuracy,
    day, month, year, hour,
                    minute FROM attempts WHERE person_id = ? """ + mode,
                                           (person_id,)).fetchall()
    return attempts


def get_max_speed_accuracy(connection, person_id):
    """Получение максимальных скорости и точности пользователя по id"""

    speed, accuracy = connection.cursor().execute(
        f"""SELECT MAX(speed), accuracy FROM attempts 
                                        WHERE
                    person_id = {person_id}""").fetchone()
    speed = 0 if speed is None else speed
    accuracy = 0 if accuracy is None else accuracy
    return speed, accuracy
