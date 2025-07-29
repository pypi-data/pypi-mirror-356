import tkinter as tk  # Импортируем модуль tkinter для создания GUI
from tkinter import ttk, messagebox, simpledialog  # Импортируем виджеты и диалоги tkinter
import pyodbc  # Импортируем pyodbc для работы с базой данных SQL Server
from PIL import Image, ImageTk  # Импортируем PIL для работы с изображениями
import os  # Импортируем os для работы с файловой системой

# Строка подключения к базе данных SQL Server
# Чтобы подключиться к другой базе данных, измените:
#   - SERVER=DESKTOP-06LI4B2   # на имя вашего SQL Server (например, localhost, localhost\\SQLEXPRESS, или IP-адрес)
#   - DATABASE=demo            # на имя вашей базы данных
#   - Trusted_Connection=yes   # если нужна SQL-аутентификация, замените на UID=логин;PWD=пароль;
DB_CONNECTION = 'DRIVER={SQL Server};SERVER=DESKTOP-06LI4B2;DATABASE=demo;Trusted_Connection=yes;'

# Цвета интерфейса
MAIN_BG = '#FFFFFF'  # Основной фон
SECONDARY_BG = '#F4E8D3'  # Вторичный фон
ACCENT_COLOR = '#67BA80'  # Акцентный цвет

# Шрифт по умолчанию
DEFAULT_FONT = ('Segoe UI', 10)  # Кортеж: название шрифта и размер

def get_connection():  # Функция для получения соединения с базой данных
    return pyodbc.connect(DB_CONNECTION)  # Возвращает объект соединения

def fetch_all(table):  # Функция для получения всех строк из таблицы
    with get_connection() as conn:  # Открываем соединение с БД
        cur = conn.cursor()  # Создаем курсор
        cur.execute(f"SELECT * FROM {table}")  # Выполняем SQL-запрос на выборку всех данных
        return cur.fetchall()  # Возвращаем все строки результата

def get_columns(table):  # Функция для получения списка колонок таблицы
    with get_connection() as conn:  # Открываем соединение с БД
        cur = conn.cursor()  # Создаем курсор
        cur.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}' ORDER BY ORDINAL_POSITION")  # Запрашиваем имена колонок
        return [row[0] for row in cur.fetchall()]  # Возвращаем список имен колонок

def insert_row(table, values):  # Функция для вставки новой строки в таблицу
    with get_connection() as conn:  # Открываем соединение с БД
        cur = conn.cursor()  # Создаем курсор
        cols = get_columns(table)  # Получаем список колонок
        placeholders = ','.join(['?'] * len(cols))  # Формируем строку плейсхолдеров для SQL
        cur.execute(f"INSERT INTO {table} VALUES ({placeholders})", values)  # Выполняем SQL-запрос на вставку
    conn.commit()  # Сохраняем изменения

def update_row(table, pk_col, pk_val, values):  # Функция для обновления строки по первичному ключу
    with get_connection() as conn:  # Открываем соединение с БД
        cur = conn.cursor()  # Создаем курсор
        cols = get_columns(table)  # Получаем список колонок
        set_expr = ', '.join([f"[{col}]=?" for col in cols if col != pk_col])  # Формируем выражение SET для SQL
        update_values = [v for i, v in enumerate(values) if cols[i] != pk_col]  # Значения для обновления (кроме PK)
        update_values.append(pk_val)  # Добавляем значение PK для WHERE
        cur.execute(f"UPDATE {table} SET {set_expr} WHERE [{pk_col}]=?", update_values)  # Выполняем SQL-запрос на обновление
    conn.commit()  # Сохраняем изменения

def delete_row(table, pk_col, pk_val):  # Функция для удаления строки по первичному ключу
    with get_connection() as conn:  # Открываем соединение с БД
        cur = conn.cursor()  # Создаем курсор
        cur.execute(f"DELETE FROM {table} WHERE [{pk_col}]=?", (pk_val,))  # Выполняем SQL-запрос на удаление
        conn.commit()  # Сохраняем изменения

class TableTab:  # Класс для отображения одной вкладки с таблицей
    def __init__(self, parent, table, tab_name=None):  # Конструктор класса
        self.table = table  # Название таблицы
        self.columns = get_columns(table)  # Получение колонок таблицы
        self.pk_col = self.columns[0]  # Первичный ключ (первая колонка)
        self.frame = ttk.Frame(parent)  # Создание фрейма для вкладки
        self.frame.configure(style="Secondary.TFrame")  # Применение стиля к фрейму
        
        # Добавление названия таблицы вверху (используем tab_name, если есть)
        display_name = tab_name if tab_name else table  # Русское название или имя таблицы
        table_label = tk.Label(self.frame, text=display_name, font=DEFAULT_FONT, bg=SECONDARY_BG)  # Метка с названием
        table_label.pack(side='top', pady=5)  # Размещение названия таблицы вверху
        
        # Добавление логотипа вверху
        try:
            logo_img = Image.open("Мастер пол.ico")  # Открытие изображения логотипа
            logo_img = logo_img.resize((50, 50), Image.LANCZOS)  # Изменение размера логотипа
            logo_photo = ImageTk.PhotoImage(logo_img)  # Создание фотоизображения
            logo_label = tk.Label(self.frame, image=logo_photo, bg=SECONDARY_BG)  # Метка для логотипа
            logo_label.image = logo_photo  # Сохраняем ссылку на изображение, чтобы не удалилось сборщиком мусора
            logo_label.pack(side='top', pady=10)  # Размещение логотипа вверху
        except Exception as e:
            print(f"Error loading logo: {e}")  # Если ошибка загрузки логотипа, выводим в консоль
        
        # Настройка стиля для дерева (таблицы)
        style = ttk.Style()  # Создаем объект стиля
        # Для вкладки Партнеры используем меньший шрифт
        if self.table == 'Partners_import':
            tree_font = ("Segoe UI", 8)
            col_width = 80
        else:
            tree_font = DEFAULT_FONT
            col_width = 120
        style.configure("Treeview", 
                       background=MAIN_BG,  # Цвет фона
                       foreground="black",  # Цвет текста
                       rowheight=22 if self.table == 'Partners_import' else 25,  # Меньше высота строки для партнеров
                       fieldbackground=MAIN_BG,  # Цвет поля
                       font=tree_font)  # Шрифт
        style.configure("Treeview.Heading", 
                       font=tree_font,  # Шрифт заголовка
                       background=SECONDARY_BG)  # Фон заголовка
        style.map('Treeview',
                 background=[('selected', ACCENT_COLOR)])  # Цвет выделения
        style.configure("Secondary.TFrame", background=SECONDARY_BG)  # Стиль для вторичного фрейма
        
        # Создание фрейма для дерева и полосы прокрутки
        tree_frame = ttk.Frame(self.frame, style="Secondary.TFrame")  # Фрейм для таблицы
        tree_frame.pack(fill='both', expand=True, side='left')  # Размещение фрейма
        
        # Добавление горизонтальной полосы прокрутки
        h_scrollbar = ttk.Scrollbar(tree_frame, orient='horizontal')  # Горизонтальный скроллбар
        h_scrollbar.pack(side='bottom', fill='x')  # Размещение скроллбара
        
        self.tree = ttk.Treeview(tree_frame, columns=self.columns, show='headings', xscrollcommand=h_scrollbar.set)  # Создание таблицы
        h_scrollbar.config(command=self.tree.xview)  # Привязка скроллбара к таблице
        
        # Настройка ширины колонок
        for col in self.columns:
            self.tree.heading(col, text=col)  # Заголовок колонки
            self.tree.column(col, width=col_width)  # Ширина колонки
        
        self.tree.pack(fill='both', expand=True)  # Размещение таблицы
        self.tree.bind('<Double-1>', self.on_edit)  # Привязка события двойного клика для редактирования
        
        # Создание фрейма для кнопок
        btn_frame = ttk.Frame(self.frame, style="Secondary.TFrame")  # Фрейм для кнопок
        btn_frame.pack(side='right', fill='y')  # Размещение фрейма кнопок
        
        # Настройка стиля кнопок
        style.configure("Custom.TButton",
                       font=DEFAULT_FONT,
                       background=ACCENT_COLOR)  # Стиль кнопок
        
        # Добавление кнопок
        ttk.Button(btn_frame, text="Добавить", command=self.on_add, style="Custom.TButton").pack(fill='x', pady=2)  # Кнопка добавления
        ttk.Button(btn_frame, text="Изменить", command=self.on_edit, style="Custom.TButton").pack(fill='x', pady=2)  # Кнопка изменения
        ttk.Button(btn_frame, text="Удалить", command=self.on_delete, style="Custom.TButton").pack(fill='x', pady=2)  # Кнопка удаления
        
        self.load_data()  # Загрузка данных в таблицу

    def load_data(self):  # Метод для загрузки данных в таблицу
        for row in self.tree.get_children():  # Удаляем все старые строки
            self.tree.delete(row)
        for row in fetch_all(self.table):  # Для каждой строки из БД
            self.tree.insert('', 'end', values=[str(val) for val in row])  # Вставляем строку, преобразуя значения в строки

    def on_add(self):  # Метод для добавления новой строки
        # Создаем новое окно для ввода всех полей сразу
        dialog = tk.Toplevel(self.frame)
        dialog.title("Добавить запись")
        entries = {}
        small_font = ("Segoe UI", 9)  # Меньший шрифт для компактности
        for i, col in enumerate(self.columns):
            tk.Label(dialog, text=col, font=small_font).grid(row=i, column=0, padx=3, pady=2, sticky='e')
            entry = tk.Entry(dialog, font=small_font, width=18)  # Меньший размер поля
            entry.grid(row=i, column=1, padx=3, pady=2)
            entries[col] = entry
        def submit():
            values = [entries[col].get() for col in self.columns]
            if any(val == '' for val in values):
                messagebox.showerror("Ошибка", "Все поля должны быть заполнены!", parent=dialog)
                return
            try:
                insert_row(self.table, values)
                self.load_data()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Ошибка", str(e), parent=dialog)
        tk.Button(dialog, text="Добавить", command=submit, font=small_font).grid(row=len(self.columns), column=0, columnspan=2, pady=6)
        dialog.resizable(False, False)  # Запретить изменение размера окна
        dialog.grab_set()
        dialog.wait_window()

    def on_edit(self, event=None):  # Метод для редактирования строки
        selected = self.tree.selection()  # Получаем выбранную строку
        if not selected:  # Если ничего не выбрано
            messagebox.showinfo("Выберите запись", "Сначала выберите строку для изменения.")
            return
        old_values = self.tree.item(selected[0])['values']  # Старые значения
        # Создаем новое окно для редактирования всех полей сразу
        dialog = tk.Toplevel(self.frame)
        dialog.title("Изменить запись")
        entries = {}
        small_font = ("Segoe UI", 9)  # Меньший шрифт для компактности
        for i, col in enumerate(self.columns):
            tk.Label(dialog, text=col, font=small_font).grid(row=i, column=0, padx=3, pady=2, sticky='e')
            entry = tk.Entry(dialog, font=small_font, width=18)
            entry.insert(0, old_values[i])
            entry.grid(row=i, column=1, padx=3, pady=2)
            entries[col] = entry
        def submit():
            new_values = [entries[col].get() for col in self.columns]
            if any(val == '' for val in new_values):
                messagebox.showerror("Ошибка", "Все поля должны быть заполнены!", parent=dialog)
                return
            try:
                update_row(self.table, self.pk_col, old_values[0], new_values)
                self.load_data()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Ошибка", str(e), parent=dialog)
        tk.Button(dialog, text="Сохранить", command=submit, font=small_font).grid(row=len(self.columns), column=0, columnspan=2, pady=6)
        dialog.resizable(False, False)  # Запретить изменение размера окна
        dialog.grab_set()
        dialog.wait_window()

    def on_delete(self):  # Метод для удаления строки
        selected = self.tree.selection()  # Получаем выбранную строку
        if not selected:  # Если ничего не выбрано
            messagebox.showinfo("Выберите запись", "Сначала выберите строку для удаления.")
            return
        values = self.tree.item(selected[0])['values']  # Значения выбранной строки
        if messagebox.askyesno("Удалить", "Удалить выбранную запись?"):  # Подтверждение удаления
            try:
                delete_row(self.table, self.pk_col, values[0])  # Удаляем строку из БД
                self.load_data()  # Обновляем таблицу
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))  # Показываем ошибку

def main():  # Главная функция приложения
    root = tk.Tk()  # Создаем главное окно
    root.title("Система управления заявками")  # Заголовок окна
    root.geometry("900x500")  # Размер окна
 
    try:
        if os.path.exists("icon.ico"):  # Если есть иконка
            root.iconbitmap("icon.ico")  # Устанавливаем иконку
    except:
        pass  # Игнорируем ошибки

    root.configure(bg=MAIN_BG)  # Устанавливаем фон окна
    
    style = ttk.Style()  # Создаем объект стиля
    style.configure("TNotebook", background=MAIN_BG)  # Стиль для вкладок
    style.configure("TNotebook.Tab", 
                   font=DEFAULT_FONT,
                   background=SECONDARY_BG,
                   padding=[10, 2])  # Стиль для заголовков вкладок
    
    notebook = ttk.Notebook(root)  # Создаем виджет вкладок
    notebook.pack(fill='both', expand=True, padx=10, pady=10)  # Размещаем вкладки
    
    try:
        if os.path.exists("logo.png"):  # Если есть логотип
            logo_img = Image.open("logo.png")  # Открываем логотип
            logo_photo = ImageTk.PhotoImage(logo_img)  # Создаем фотоизображение
            logo_label = tk.Label(root, image=logo_photo, bg=MAIN_BG)  # Метка с логотипом
            logo_label.image = logo_photo  # Сохраняем ссылку на изображение
            logo_label.pack(pady=10)  # Размещаем логотип
    except:
        pass  # Игнорируем ошибки

    # Список таблиц и их русских названий для вкладок
    tables = [
        ('Product_type_import', 'Типы продукции'),
        ('Partners_import', 'Партнеры'),
        ('Products_import', 'Продукция'),
        ('Partner_products_import', 'Продажи партнеров'),
        ('Material_type_import', 'Типы материалов')
    ]
    
    for table, tab_name in tables:  # Для каждой таблицы
        tab = TableTab(notebook, table, tab_name)  # Создаем вкладку
        notebook.add(tab.frame, text=tab_name)  # Добавляем вкладку с русским названием

    root.mainloop()  # Запускаем главный цикл приложения

if __name__ == '__main__':  # Если файл запущен как основная программа
    main()  # Запускаем main()