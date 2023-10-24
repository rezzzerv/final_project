import tkinter as tk
from enum import Enum

DB_NAME = "employees.db"


class WindowSize(Enum):
    MAIN_WINDOW: str = "800x600"
    SEARCH_WINDOW: str = "300x100"
    ADD_WINDOW: str = "400x200"


class Column(Enum):
    ID: str = "ID"
    NAME: str = "name"
    PHONE: str = "phone"
    EMAIL: str = "email"
    SALARY: str = "salary"

    ID_TEXT: str = "ID"
    NAME_TEXT: str = "ФИО"
    PHONE_TEXT: str = "Телефон"
    EMAIL_TEXT: str = "E-mail"
    SALARY_TEXT: str = "Оклад"

    HEIGHT_SMALL: int = 45
    WIDTH_SMALL: int = 45
    WIDTH: int = 150
    WIDTH_LARGE: int = 300
    ANCHOR_CENTER: tk.CENTER = tk.CENTER

    @classmethod
    def get_col_names(cls):
        return (
            (cls.ID, cls.ID_TEXT),
            (cls.NAME, cls.NAME_TEXT),
            (cls.PHONE, cls.PHONE_TEXT),
            (cls.EMAIL, cls.EMAIL_TEXT),
            (cls.SALARY, cls.SALARY_TEXT),
        )

    @classmethod
    def get_col_params(cls):
        return (
            (cls.ID, cls.WIDTH_SMALL, cls.ANCHOR_CENTER),
            (cls.NAME, cls.WIDTH_LARGE, cls.ANCHOR_CENTER),
            (cls.PHONE, cls.WIDTH, cls.ANCHOR_CENTER),
            (cls.EMAIL, cls.WIDTH, cls.ANCHOR_CENTER),
            (cls.SALARY, cls.WIDTH, cls.ANCHOR_CENTER),
        )


class BorderSize(Enum):
    TOOLBAR: int = 5
    ICON: int = 1


class Color(Enum):
    TOOLBAR_BG: str = "#d7d7d7"
    ICON_BG: str = "#d7d7d7"
    WHITE: str = "White"


class ImgPath(Enum):
    ADD: str = "icons/add.png"
    CHANGE: str = "icons/change.png"
    DELETE: str = "icons/delete.png"
    SEARCH: str = "icons/search.png"
    UPDATE: str = "icons/update.png"


class SQLCommand(Enum):
    CREATE_TABLE_EMPLOYEES: str = """
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY NOT NULL,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            salary TEXT NOT NULL
        )
    """
    INSERT_EMPLOYEE: str = (
        """INSERT INTO employees (name, phone, email, salary)
        VALUES (?, ?, ?, ?)"""
    )
    UPDATE_RECORD: str = (
        """UPDATE employees
        SET name=?, phone=?, email=?, salary=? WHERE  ID=?"""
    )
    DELETE_RECORD: str = """DELETE FROM employees WHERE ID=?"""
    SEARCH_BY_NAME: str = """SELECT * FROM employees WHERE name LIKE ?"""
    SELECT_ALL_EMPLOYEES: str = """SELECT * FROM employees"""
    DEFAULT_DATA: str = """SELECT * FROM employees WHERE ID=?"""


class ButtonText(Enum):
    ADD: str = "Добавить"
    SEARCH: str = "Найти"
    CLOSE: str = "Закрыть"
    EDIT: str = "Редактировать"


class LabelText(Enum):
    FIO: str = "ФИО: "
    PHONE: str = "Телефон: "
    EMAIL: str = "E-mail: "
    SALARY: str = "Оклад: "
    TITLE: str = "EmpManager V1.0"
    EDIT_WINDOW_TITLE: str = "Редактировать данные сотрудника"
    ADD_EMPLOYEE: str = "Добавить"
    UPDATE_EMPLOYEE: str = "Редактировать"
    SEARCH_EMPLOYEE: str = "Поиск"


class EmployeeFixture(Enum):
    FIXTURE_DATA: list[tuple[str, str, str, str], ...] = [
        ("Александров Михаил Сергеевич",
         "+79001234567", "user1@mail.com", "95000"),
        ("Николаева Мария Константиновна",
         "+79001234568", "user2@mail.com", "120000"),
        ("Иванов Петр Александрович",
         "+79001234569", "user3@mail.com", "110000"),
        ("Смирнова Ольга Николаевна",
         "+79001234570", "user4@mail.com", "100000"),
        ("Соколов Денис Владимирович",
         "+79001234571", "user5@mail.com", "95000"),
        ("Попова Анна Игоревна",
         "+79001234572", "user6@mail.com", "130000"),
        ("Кузнецов Андрей Артемович",
         "+79001234573", "user7@mail.com", "110000"),
        ("Васильева Екатерина Сергеевна",
         "+79001234574", "user8@mail.com", "105000"),
        ("Петров Максим Валерьевич",
         "+79001234575", "user9@mail.com", "95000"),
        ("Соловьев Игорь Олегович",
         "+79001234576", "user10@mail.com", "140000"),
        ("Морозов Артем Вячеславович",
         "+79001234577", "user11@mail.com", "125000"),
        ("Давыдов Егор Андреевич",
         "+79001234578", "user12@mail.com", "95000"),
        ("Захаров Даниил Ильич",
         "+79001234579", "user13@mail.com", "135000"),
        ("Борисова Маргарита Ивановна",
         "+79001234580", "user14@mail.com", "95000"),
        ("Алексеев Николай Олегович",
         "+79001234581", "user15@mail.com", "115000"),
        ("Сидорова Алёна Андреевна",
         "+79001234582", "user16@mail.com", "120000"),
        ("Гаврилов Владислав Игоревич",
         "+79001234583", "user17@mail.com", "95000"),
        ("Тарасова Кристина Денисовна",
         "+79001234584", "user18@mail.com", "95000"),
        ("Фёдоров Глеб Владимирович",
         "+79001234585", "user19@mail.com", "95000"),
        ("Архипов Степан Михайлович",
         "+79001234586", "user20@mail.com", "95000")
    ]
