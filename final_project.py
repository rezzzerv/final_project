import sqlite3
import tkinter as tk
from tkinter import ttk

from enums import (BorderSize,
                   ButtonText,
                   Color,
                   Column,
                   DB_NAME,
                   EmployeeFixture,
                   ImgPath,
                   LabelText,
                   SQLCommand,
                   WindowSize)


class Main(tk.Frame):
    """
    Главное окно приложения.
    Отображает список сотрудников, позволяет добавлять,
    редактировать и удалять записей.
    """

    def __init__(self, root) -> None:
        super().__init__(root)
        self.init_main()
        self.db: EmployeeDB = db
        self.view_records()

    def init_main(self) -> None:
        """
        Инициализация главного окна и его компонентов.
        """
        toolbar = tk.Frame(bg=Color.TOOLBAR_BG.value,
                           bd=BorderSize.TOOLBAR.value)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Кнопка "Добавить"
        self.add_img = tk.PhotoImage(file=ImgPath.ADD.value)
        btn_add = tk.Button(toolbar,
                            bg=Color.ICON_BG.value,
                            bd=BorderSize.ICON.value,
                            image=self.add_img,
                            command=self.open_child)
        btn_add.pack(side=tk.LEFT)

        # Кнопка "Редактировать"
        self.edit_img = tk.PhotoImage(file=ImgPath.CHANGE.value)
        btn_edit = tk.Button(toolbar,
                             bg=Color.ICON_BG.value,
                             bd=BorderSize.ICON.value,
                             image=self.edit_img,
                             command=self.open_update_dialog)
        btn_edit.pack(side=tk.LEFT)

        # Кнопка "Удалить"
        self.delete_img = tk.PhotoImage(file=ImgPath.DELETE.value)
        btn_del = tk.Button(toolbar,
                            bg=Color.ICON_BG.value,
                            bd=BorderSize.ICON.value,
                            image=self.delete_img,
                            command=self.delete_records)
        btn_del.pack(side=tk.LEFT)

        # Кнопка "Поиск"
        self.search_img = tk.PhotoImage(file=ImgPath.SEARCH.value)
        btn_search = tk.Button(toolbar,
                               bg=Color.ICON_BG.value,
                               bd=BorderSize.ICON.value,
                               image=self.search_img,
                               command=self.open_search)
        btn_search.pack(side=tk.LEFT)

        # Кнопка "Обновить"
        self.refresh_img = tk.PhotoImage(file=ImgPath.UPDATE.value)
        btn_refresh = tk.Button(toolbar,
                                bg=Color.ICON_BG.value,
                                bd=BorderSize.ICON.value,
                                image=self.refresh_img,
                                command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)
        self.tree = ttk.Treeview(
            self,
            # Название столбцов
            columns=[elem[0].value for elem in Column.get_col_names()],
            height=int(Column.HEIGHT_SMALL.value),
            show='headings'
        )

        # Настройка параметров колонок
        for item, width, anchor in Column.get_col_params():
            self.tree.column(item.value,
                             width=int(width.value),
                             anchor=anchor.value)

        # Наименования колонок
        for item, text in Column.get_col_names():
            self.tree.heading(item.value, text=text.value)

        self.tree.pack(side=tk.LEFT)

    def view_records(self) -> None:
        """
        Отображает записи из базы данных в виде списка сотрудников в TreeView.
        """
        self.db.cur.execute(SQLCommand.SELECT_ALL_EMPLOYEES.value)

        # Очистка таблицы
        [self.tree.delete(i)
         for i in self.tree.get_children()]

        # Вставка данных из базы
        [self.tree.insert('', "end", values=row)
         for row in self.db.cur.fetchall()]

    def records(self, name, phone, email, salary) -> None:
        """
        Добавляет новую запись о сотрудниках в базу данных.
        Обновляет отображение сотрудников.

        :param name: ФИО сотрудника
        :param phone: Номер телефона
        :param email: Электронная почта
        :param salary: Заработная плата
        """
        self.db.insert_data(name, phone, email, salary)
        self.view_records()

    def update_record(self, name, phone, email, salary) -> None:
        """
        Обновляет запись о сотруднике в базе данных.
        Обновляет отображение сотрудников.

        :param name: Новое ФИО сотрудника
        :param phone: Новый номер телефона
        :param email: Новая электронная почта
        :param salary: Новая заработная плата
        """
        id = self.tree.set(self.tree.selection()[0], '#1')
        self.db.cur.execute(
            SQLCommand.UPDATE_RECORD.value,
            (name, phone, email, salary, id)
        )
        self.db.conn.commit()
        self.view_records()

    def delete_records(self) -> None:
        """
        Удаляет выбранные записи о сотруднике из базы данных.
        Обновляет отображение сотрудников.
        """
        for row in self.tree.selection():
            self.db.cur.execute(
                SQLCommand.DELETE_RECORD.value,
                (self.tree.set(row, '#1'),)
            )
            self.db.conn.commit()
            self.view_records()

    def search_records(self, name) -> None:
        """
        Выполняет поиск сотрудников в базе данных по имени.
        Обновляет отображение найденных сотрудников.

        :param name: Имя сотрудника для поиска
        """
        self.db.cur.execute(
            SQLCommand.SEARCH_BY_NAME.value,
            (('%' + name + '%'),)
        )

        [self.tree.delete(i)
         for i in self.tree.get_children()]

        [self.tree.insert('', 'end', values=row)
         for row in self.db.cur.fetchall()]

    def open_child(self) -> None:
        """
        Открывает окно для добавления нового сотрудника.
        """
        Child()

    def open_update_dialog(self) -> None:
        """
        Открывает окно для обновления существующего сотрудника.
        """
        Update()

    def open_search(self) -> None:
        """
        Открывает окно для выполнения поиска сотрудников.
        """
        Search()


class Child(tk.Toplevel):
    """
    Окно для добавления нового сотрудника.
    """

    def __init__(self) -> None:
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self) -> None:
        """
        Инициализация окна добавления нового сотрудника и его компонентов.
        """
        self.title(LabelText.ADD_EMPLOYEE.value)
        self.geometry(WindowSize.ADD_WINDOW.value)
        self.grab_set()
        self.focus_set()

        label_name = tk.Label(self, text=LabelText.FIO.value)
        label_name.place(x=50, y=50)
        label_phone = tk.Label(self, text=LabelText.PHONE.value)
        label_phone.place(x=50, y=80)
        label_email = tk.Label(self, text=LabelText.EMAIL.value)
        label_email.place(x=50, y=110)
        label_salary = tk.Label(self, text=LabelText.SALARY.value)
        label_salary.place(x=50, y=140)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)
        self.entry_phone = ttk.Entry(self)
        self.entry_phone.place(x=200, y=80)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=110)
        self.entry_salary = ttk.Entry(self)
        self.entry_salary.place(x=200, y=140)

        # Кнопка закрытия
        self.btn_cancel = ttk.Button(self,
                                     text=ButtonText.CLOSE.value,
                                     command=self.destroy)
        self.btn_cancel.place(x=300, y=170)

        # Кнопка добавления
        self.btn_add = ttk.Button(self, text=ButtonText.ADD.value)
        self.btn_add.place(x=220, y=170)
        self.btn_add.bind(
            '<Button-1>',
            lambda event: self.view.records(self.entry_name.get(),
                                            self.entry_phone.get(),
                                            self.entry_email.get(),
                                            self.entry_salary.get())
        )


class Update(Child):
    """
    Окно для редактирования сотрудника.
    Унаследовано от класса Child.
    """

    def __init__(self) -> None:
        super().__init__()
        self.init_update()
        self.db = db

    def init_update(self) -> None:
        """
        Инициализация окна редактирования сотрудника и его компонентов.
        """
        self.title(LabelText.EDIT_WINDOW_TITLE.value)
        self.btn_add.destroy()

        self.btn_upd = ttk.Button(self, text=ButtonText.EDIT.value)
        self.btn_upd.bind(
            '<Button-1>',
            lambda event: self.view.update_record(
                self.entry_name.get(),
                self.entry_phone.get(),
                self.entry_email.get(),
                self.entry_salary.get())
        )
        self.btn_upd.bind(
            '<Button-1>',
            lambda event: self.destroy(), add='+'
        )
        self.btn_upd.place(x=170, y=170)

    def default_data(self) -> None:
        id = self.view.tree.set(
            self.view.tree.selection()[0],
            '#1'
        )
        self.db.cur.execute(
            SQLCommand.DEFAULT_DATA.value,
            (id,)
        )
        row = self.db.cur.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_phone.insert(0, row[2])
        self.entry_email.insert(0, row[3])
        self.entry_salary.insert(0, row[4])


class Search(tk.Toplevel):
    """
    Окно для поиска сотрудников.
    """

    def __init__(self) -> None:
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self) -> None:
        """
        Инициализация окна поиска сотрудников и его компонентов.
        """
        self.title(LabelText.SEARCH_EMPLOYEE.value)
        self.geometry(WindowSize.SEARCH_WINDOW.value)
        self.resizable(width=False, height=False)
        self.grab_set()
        self.focus_set()

        label_name = tk.Label(self, text=LabelText.FIO.value)
        label_name.place(x=20, y=20)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=70, y=20)

        # Кнопка закрытия
        self.btn_cancel = ttk.Button(
            self,
            text=ButtonText.CLOSE.value,
            command=self.destroy
        )
        self.btn_cancel.place(x=200, y=70)
        self.btn_search = ttk.Button(
            self, text=ButtonText.SEARCH.value
        )
        self.btn_search.place(x=70, y=70)
        self.btn_search.bind(
            "<Button-1>",
            lambda event: self.view.search_records(self.entry_name.get())
        )


class EmployeeDB:
    """
    Класс для работы с базой данных сотрудников.
    """

    def __init__(self) -> None:
        self.conn = sqlite3.connect(DB_NAME)
        self.cur = self.conn.cursor()
        self.cur.execute(SQLCommand.CREATE_TABLE_EMPLOYEES.value)
        self.conn.commit()

    def insert_data(self, name, phone, email, salary) -> None:
        """
        Добавляет нового сотрудника в базу данных.

        :param name: ФИО сотрудника
        :param phone: Номер телефон
        :param email: Электронная почта
        :param salary: Заработная плата
        """
        self.cur.execute(
            SQLCommand.INSERT_EMPLOYEE.value,
            (name, phone, email, salary)
        )
        self.conn.commit()

    def _import_data(self):
        """Заполняет базу данных данными о сотрудниках."""
        for employee in EmployeeFixture.FIXTURE_DATA.value:
            self.insert_data(*employee)
            self.conn.commit()


if __name__ == "__main__":
    root = tk.Tk()
    db = EmployeeDB()

    # db._import_data()  # Если удалили БД,
    # вызовите этот метод один раз, чтобы заполнить БД с тестовыми данными.

    app = Main(root)
    app.pack()
    root.title(LabelText.TITLE.value)
    root.geometry(WindowSize.MAIN_WINDOW.value)
    root.resizable(width=False, height=False)
    root.configure(bg=Color.WHITE.value)
    root.mainloop()
