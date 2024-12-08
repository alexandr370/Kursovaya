import psycopg2
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QLineEdit, QPushButton, QLabel, QMessageBox, QTableWidget, QTableWidgetItem)
from PyQt6.QtCore import Qt
import sys


# Подключение к базе данных
def get_db_connection():
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="password",
        host="localhost",
        port="5432"
    )


def check_db_connection():
    try:
        conn = get_db_connection()
        conn.close()
        return True
    except Exception as e:
        QMessageBox.critical(None, "Ошибка подключения", f"База данных недоступна: {str(e)}")
        return False


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Авторизация")

        # Центральный виджет и макет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Поле ввода имени пользователя
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Email")
        layout.addWidget(self.username_input)

        # Поле ввода пароля
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        # Кнопка входа
        self.login_button = QPushButton("Войти")
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)

        # Кнопка регистрации
        self.register_button = QPushButton("Регистрация")
        self.register_button.clicked.connect(self.open_register_window)
        layout.addWidget(self.register_button)

    def handle_login(self):
        email = self.username_input.text()
        password = self.password_input.text()

        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(
                "SELECT * FROM \"TouristSchema\".\"users\" WHERE email=%s AND password=%s",
                (email, password)
            )
            user = cursor.fetchone()
            connection.close()

            if user:
                QMessageBox.information(self, "Успех", "Вы успешно вошли!")
                self.open_profile_window(user[0], email)
            else:
                QMessageBox.warning(self, "Ошибка", "Неверный email или пароль!")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось подключиться к базе данных: {str(e)}")

    def open_register_window(self):
        self.register_window = RegisterWindow()
        self.register_window.show()

    def open_profile_window(self, user_id, email):
        self.profile_window = ProfileWindow(user_id, email)
        self.profile_window.show()
        self.close()


class RegisterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Регистрация")

        # Центральный виджет и макет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Поле ввода email
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        layout.addWidget(self.email_input)

        # Поле ввода пароля
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        # Поле подтверждения пароля
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Подтвердите пароль")
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.confirm_password_input)

        # Кнопка регистрации
        self.register_button = QPushButton("Зарегистрироваться")
        self.register_button.clicked.connect(self.handle_register)
        layout.addWidget(self.register_button)

    def handle_register(self):
        email = self.email_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if not email or not password:
            QMessageBox.warning(self, "Ошибка", "Все поля обязательны для заполнения!")
            return

        if password != confirm_password:
            QMessageBox.warning(self, "Ошибка", "Пароли не совпадают!")
            return

        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO \"TouristSchema\".\"users\" (email, password) VALUES (%s, %s)",
                (email, password)
            )
            connection.commit()
            connection.close()

            QMessageBox.information(self, "Успех", "Регистрация успешна!")
            self.close()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось зарегистрироваться: {str(e)}")


class ProfileWindow(QMainWindow):
    def __init__(self, user_id, email):
        super().__init__()
        self.user_id = user_id
        self.email = email
        self.setWindowTitle("Профиль")

        # Центральный виджет и макет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Приветственное сообщение
        welcome_label = QLabel(f"Добро пожаловать, {email}!")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(welcome_label)

        # Кнопка просмотра паспортных данных
        passport_button = QPushButton("Паспортные данные")
        passport_button.clicked.connect(self.open_passport_window)
        layout.addWidget(passport_button)

        # Кнопка просмотра туров
        tours_button = QPushButton("Доступные туры")
        tours_button.clicked.connect(self.open_tours_window)
        layout.addWidget(tours_button)

        # Кнопка просмотра истории бронирований
        booking_button = QPushButton("История бронирований")
        booking_button.clicked.connect(self.open_booking_history_window)
        layout.addWidget(booking_button)

        # Кнопка выхода
        logout_button = QPushButton("Выйти")
        logout_button.clicked.connect(self.logout)
        layout.addWidget(logout_button)

    def open_passport_window(self):
        self.passport_window = PassportWindow()
        self.passport_window.show()

    def open_tours_window(self):
        self.tours_window = ToursWindow()
        self.tours_window.show()

    def open_booking_history_window(self):
        self.booking_window = BookingHistoryWindow()
        self.booking_window.show()

    def logout(self):
        self.close()
        self.login_window = LoginWindow()
        self.login_window.show()


class PassportWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Паспортные данные")

        # Центральный виджет и макет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(
                "SELECT name, surname, patronymic, passport_series_and_number, gender, validity_period, date_of_birth, citizenship "
                "FROM \"TouristSchema\".\"passport_data\""
            )
            passport_datas = cursor.fetchall()
            connection.close()

            if passport_datas:
                self.table = QTableWidget(len(passport_datas), 8)
                self.table.setHorizontalHeaderLabels([
                    "Имя", "Фамилия", "Отчество", "Серия и номер паспорта", "Пол", "Срок действия", "Дата рождения",
                    "Гражданство"
                ])

                for row, passport_data in enumerate(passport_datas):
                    for column, value in enumerate(passport_data):
                        self.table.setItem(row, column, QTableWidgetItem(str(value)))

                layout.addWidget(self.table)
            else:
                layout.addWidget(QLabel("Паспортные данные не найдены!"))

            # Форма для добавления нового паспорта
            self.new_entry_form = QWidget()
            form_layout = QVBoxLayout()
            self.new_entry_form.setLayout(form_layout)

            # Поле для ввода user_id
            self.user_id_input = QLineEdit()
            self.user_id_input.setPlaceholderText("ID пользователя")
            form_layout.addWidget(self.user_id_input)

            # Остальные поля для нового паспорта
            self.name_input = QLineEdit()
            self.name_input.setPlaceholderText("Имя")
            form_layout.addWidget(self.name_input)

            self.surname_input = QLineEdit()
            self.surname_input.setPlaceholderText("Фамилия")
            form_layout.addWidget(self.surname_input)

            self.patronymic_input = QLineEdit()
            self.patronymic_input.setPlaceholderText("Отчество")
            form_layout.addWidget(self.patronymic_input)

            self.passport_series_number_input = QLineEdit()
            self.passport_series_number_input.setPlaceholderText("Серия и номер паспорта")
            form_layout.addWidget(self.passport_series_number_input)

            self.gender_input = QLineEdit()
            self.gender_input.setPlaceholderText("Пол")
            form_layout.addWidget(self.gender_input)

            self.validity_period_input = QLineEdit()
            self.validity_period_input.setPlaceholderText("Срок действия (YYYY-MM-DD)")
            form_layout.addWidget(self.validity_period_input)

            self.date_of_birth_input = QLineEdit()
            self.date_of_birth_input.setPlaceholderText("Дата рождения (YYYY-MM-DD)")
            form_layout.addWidget(self.date_of_birth_input)

            self.citizenship_input = QLineEdit()
            self.citizenship_input.setPlaceholderText("Гражданство")
            form_layout.addWidget(self.citizenship_input)

            # Кнопка для добавления записи
            self.add_button = QPushButton("Добавить запись")
            self.add_button.clicked.connect(self.add_passport_entry)
            form_layout.addWidget(self.add_button)

            layout.addWidget(self.new_entry_form)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить паспортные данные: {str(e)}")

    def add_passport_entry(self):
        user_id = self.user_id_input.text()
        name = self.name_input.text()
        surname = self.surname_input.text()
        patronymic = self.patronymic_input.text()
        passport_series_number = self.passport_series_number_input.text()
        gender = self.gender_input.text()
        validity_period = self.validity_period_input.text()
        date_of_birth = self.date_of_birth_input.text()
        citizenship = self.citizenship_input.text()

        # Проверка на заполнение всех полей
        if not user_id or not name or not surname or not patronymic or not passport_series_number or not gender or not validity_period or not date_of_birth or not citizenship:
            QMessageBox.warning(self, "Ошибка", "Все поля обязательны для заполнения!")
            return

        # Проверка на корректность формата даты
        try:
            from datetime import datetime
            datetime.strptime(validity_period, "%Y-%m-%d")
            datetime.strptime(date_of_birth, "%Y-%m-%d")
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Неверный формат даты! Используйте формат YYYY-MM-DD.")
            return

        # Попытка добавить запись в базу данных
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO \"TouristSchema\".\"passport_data\" (user_id, name, surname, patronymic, passport_series_and_number, gender, validity_period, date_of_birth, citizenship) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (user_id, name, surname, patronymic, passport_series_number, gender, validity_period, date_of_birth,
                 citizenship)
            )
            connection.commit()
            connection.close()

            QMessageBox.information(self, "Успех", "Запись успешно добавлена!")

            # Очистка полей ввода
            self.user_id_input.clear()
            self.name_input.clear()
            self.surname_input.clear()
            self.patronymic_input.clear()
            self.passport_series_number_input.clear()
            self.gender_input.clear()
            self.validity_period_input.clear()
            self.date_of_birth_input.clear()
            self.citizenship_input.clear()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить запись: {str(e)}")


class ToursWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Доступные туры")

        # Центральный виджет и макет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(
                "SELECT title, description, departure_location, departure_date, arrival_date, arrival_location, price, available_places "
                "FROM \"TouristSchema\".\"tours\""
            )
            tours = cursor.fetchall()
            connection.close()

            if tours:
                self.table = QTableWidget(len(tours), 8)
                self.table.setHorizontalHeaderLabels([
                    "Название", "Описание", "Место отправления", "Дата отправления", "Дата прибытия", "Место прибытия",
                    "Цена", "Свободные места"
                ])

                for row, tour in enumerate(tours):
                    for column, value in enumerate(tour):
                        self.table.setItem(row, column, QTableWidgetItem(str(value)))

                layout.addWidget(self.table)
            else:
                layout.addWidget(QLabel("Нет доступных туров."))

            # Форма для добавления нового тура
            self.new_entry_form = QWidget()
            form_layout = QVBoxLayout()
            self.new_entry_form.setLayout(form_layout)

            # Поля для ввода данных о туре
            self.title_input = QLineEdit()
            self.title_input.setPlaceholderText("Название тура")
            form_layout.addWidget(self.title_input)

            self.description_input = QLineEdit()
            self.description_input.setPlaceholderText("Описание тура")
            form_layout.addWidget(self.description_input)

            self.departure_location_input = QLineEdit()
            self.departure_location_input.setPlaceholderText("Место отправления")
            form_layout.addWidget(self.departure_location_input)

            self.departure_date_input = QLineEdit()
            self.departure_date_input.setPlaceholderText("Дата отправления (YYYY-MM-DD)")
            form_layout.addWidget(self.departure_date_input)

            self.arrival_date_input = QLineEdit()
            self.arrival_date_input.setPlaceholderText("Дата прибытия (YYYY-MM-DD)")
            form_layout.addWidget(self.arrival_date_input)

            self.arrival_location_input = QLineEdit()
            self.arrival_location_input.setPlaceholderText("Место прибытия")
            form_layout.addWidget(self.arrival_location_input)

            self.price_input = QLineEdit()
            self.price_input.setPlaceholderText("Цена")
            form_layout.addWidget(self.price_input)

            self.available_places_input = QLineEdit()
            self.available_places_input.setPlaceholderText("Свободные места")
            form_layout.addWidget(self.available_places_input)

            # Кнопка для добавления записи
            self.add_button = QPushButton("Добавить тур")
            self.add_button.clicked.connect(self.add_tour_entry)
            form_layout.addWidget(self.add_button)

            layout.addWidget(self.new_entry_form)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить туры: {str(e)}")

    def add_tour_entry(self):
        title = self.title_input.text()
        description = self.description_input.text()
        departure_location = self.departure_location_input.text()
        departure_date = self.departure_date_input.text()
        arrival_date = self.arrival_date_input.text()
        arrival_location = self.arrival_location_input.text()
        price = self.price_input.text()
        available_places = self.available_places_input.text()

        # Проверка на заполнение всех обязательных полей
        if not title or not description or not departure_location or not arrival_location or not departure_date or not arrival_date or not price or not available_places:
            QMessageBox.warning(self, "Ошибка", "Все поля обязательны для заполнения!")
            return

        # Проверка на корректность формата даты
        try:
            from datetime import datetime
            datetime.strptime(departure_date, "%Y-%m-%d")
            datetime.strptime(arrival_date, "%Y-%m-%d")
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Неверный формат даты! Используйте формат YYYY-MM-DD.")
            return

        # Проверка на корректность цены и количества мест
        try:
            price = float(price)
            available_places = int(available_places)
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Цена и количество мест должны быть числами.")
            return

        # Попытка добавить запись в базу данных
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO \"TouristSchema\".\"tours\" (title, description, departure_location, departure_date, arrival_date, arrival_location, price, available_places) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (title, description, departure_location, departure_date, arrival_date, arrival_location, price,
                 available_places)
            )
            connection.commit()
            connection.close()

            QMessageBox.information(self, "Успех", "Тур успешно добавлен!")

            # Очистка полей ввода
            self.title_input.clear()
            self.description_input.clear()
            self.departure_location_input.clear()
            self.departure_date_input.clear()
            self.arrival_date_input.clear()
            self.arrival_location_input.clear()
            self.price_input.clear()
            self.available_places_input.clear()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить тур: {str(e)}")


class BookingHistoryWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("История бронирований")

        # Центральный виджет и макет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(
                "SELECT user_id, booking_date, number_of_places, total_price, tour_id "
                "FROM \"TouristSchema\".\"booking_history\""
            )
            bookings = cursor.fetchall()
            connection.close()

            if bookings:
                self.table = QTableWidget(len(bookings), 5)
                self.table.setHorizontalHeaderLabels([
                    "ID пользователя", "Дата бронирования", "Количество мест", "Общая стоимость", "ID тура"
                ])

                for row, booking in enumerate(bookings):
                    for column, value in enumerate(booking):
                        self.table.setItem(row, column, QTableWidgetItem(str(value)))

                layout.addWidget(self.table)
            else:
                layout.addWidget(QLabel("История бронирований пуста."))

            # Форма для добавления новой записи о бронировании
            self.new_entry_form = QWidget()
            form_layout = QVBoxLayout()
            self.new_entry_form.setLayout(form_layout)

            # Поле ввода ID пользователя
            self.user_id_input = QLineEdit()
            self.user_id_input.setPlaceholderText("ID пользователя")
            form_layout.addWidget(self.user_id_input)

            # Поле ввода ID тура
            self.tour_id_input = QLineEdit()
            self.tour_id_input.setPlaceholderText("ID тура")
            form_layout.addWidget(self.tour_id_input)

            # Поле ввода даты бронирования
            self.booking_date_input = QLineEdit()
            self.booking_date_input.setPlaceholderText("Дата бронирования (YYYY-MM-DD)")
            form_layout.addWidget(self.booking_date_input)

            # Поле ввода количества мест
            self.number_of_places_input = QLineEdit()
            self.number_of_places_input.setPlaceholderText("Количество мест")
            form_layout.addWidget(self.number_of_places_input)

            # Поле ввода общей стоимости
            self.total_price_input = QLineEdit()
            self.total_price_input.setPlaceholderText("Общая стоимость")
            form_layout.addWidget(self.total_price_input)

            # Кнопка для добавления записи
            self.add_button = QPushButton("Добавить запись")
            self.add_button.clicked.connect(self.add_booking_entry)
            form_layout.addWidget(self.add_button)

            layout.addWidget(self.new_entry_form)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить историю бронирований: {str(e)}")

    def add_booking_entry(self):
        user_id = self.user_id_input.text()
        tour_id = self.tour_id_input.text()
        booking_date = self.booking_date_input.text()
        number_of_places = self.number_of_places_input.text()
        total_price = self.total_price_input.text()

        # Проверка на заполнение всех полей
        if not user_id or not tour_id or not booking_date or not number_of_places or not total_price:
            QMessageBox.warning(self, "Ошибка", "Все поля обязательны для заполнения!")
            return

        # Проверка на корректность формата даты
        try:
            from datetime import datetime
            datetime.strptime(booking_date, "%Y-%m-%d")
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Неверный формат даты! Используйте формат YYYY-MM-DD.")
            return

        # Проверка на типы данных для ID
        if not user_id.isdigit() or not tour_id.isdigit():
            QMessageBox.warning(self, "Ошибка", "ID пользователя и ID тура должны быть целыми числами.")
            return

        # Попытка добавить запись в базу данных
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO \"TouristSchema\".\"booking_history\" (user_id, tour_id, booking_date, number_of_places, total_price) "
                "VALUES (%s, %s, %s, %s, %s)",
                (int(user_id), int(tour_id), booking_date, int(number_of_places), float(total_price))
            )
            connection.commit()
            connection.close()

            QMessageBox.information(self, "Успех", "Запись успешно добавлена!")

            # Обновление таблицы
            self.table.setRowCount(self.table.rowCount() + 1)
            self.table.setItem(self.table.rowCount() - 1, 0, QTableWidgetItem(user_id))
            self.table.setItem(self.table.rowCount() - 1, 1, QTableWidgetItem(booking_date))
            self.table.setItem(self.table.rowCount() - 1, 2, QTableWidgetItem(number_of_places))
            self.table.setItem(self.table.rowCount() - 1, 3, QTableWidgetItem(total_price))
            self.table.setItem(self.table.rowCount() - 1, 4, QTableWidgetItem(tour_id))

            # Очистка полей ввода
            self.user_id_input.clear()
            self.tour_id_input.clear()
            self.booking_date_input.clear()
            self.number_of_places_input.clear()
            self.total_price_input.clear()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить запись: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    login_window = LoginWindow()
    login_window.show()

    sys.exit(app.exec())
