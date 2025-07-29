#import sqlite3
#
#def create_database():
#    with sqlite3.connect("company.db") as conn:
#        cursor = conn.cursor()
#
#        # Таблица пользователей
#        cursor.execute("""
#        CREATE TABLE IF NOT EXISTS users (
#            id INTEGER PRIMARY KEY AUTOINCREMENT,
#            login TEXT UNIQUE NOT NULL,
#            password TEXT NOT NULL,
#            role TEXT NOT NULL
#        )
#        """)
#
#        # Таблица отделов
#        cursor.execute("""
#        CREATE TABLE IF NOT EXISTS departments (
#            id INTEGER PRIMARY KEY AUTOINCREMENT,
#            name TEXT NOT NULL UNIQUE,
#            description TEXT
#        )
#        """)
#
#        # Таблица сотрудников
#        cursor.execute("""
#        CREATE TABLE IF NOT EXISTS employees (
#            id INTEGER PRIMARY KEY AUTOINCREMENT,
#            full_name TEXT NOT NULL,
#            position TEXT,
#            user_id INTEGER,
#            department_id INTEGER,
#            FOREIGN KEY (user_id) REFERENCES users(id),
#            FOREIGN KEY (department_id) REFERENCES departments(id)
#        )
#        """)
#
#        # Добавление тестовых пользователей
#        users = [
#            ('admin', 'adminpass', 'admin'),
#            ('johndoe', 'password123', 'user'),
#            ('janedoe', 'securepass', 'user')
#        ]
#        cursor.executemany("INSERT OR IGNORE INTO users (login, password, role) VALUES (?, ?, ?)", users)
#
#        # Добавление отделов
#        departments = [
#            ('IT', 'Отдел информационных технологий'),
#            ('HR', 'Отдел кадров'),
#            ('Sales', 'Отдел продаж')
#        ]
#        cursor.executemany("INSERT OR IGNORE INTO departments (name, description) VALUES (?, ?)", departments)
#
#        # Получаем id пользователей и отделов для вставки сотрудников
#        cursor.execute("SELECT id FROM users WHERE login = 'johndoe'")
#        johndoe_id = cursor.fetchone()[0]
#
#        cursor.execute("SELECT id FROM users WHERE login = 'janedoe'")
#        janedoe_id = cursor.fetchone()[0]
#
#        cursor.execute("SELECT id FROM departments WHERE name = 'IT'")
#        it_dept_id = cursor.fetchone()[0]
#
#        cursor.execute("SELECT id FROM departments WHERE name = 'HR'")
#        hr_dept_id = cursor.fetchone()[0]
#
#        # Добавление сотрудников
#        employees = [
#            ('Джон Доу', 'Программист', johndoe_id, it_dept_id),
#            ('Джейн Доу', 'HR-специалист', janedoe_id, hr_dept_id)
#        ]
#        cursor.executemany("""
#            INSERT OR IGNORE INTO employees (full_name, position, user_id, department_id)
#            VALUES (?, ?, ?, ?)
#        """, employees)
#
#        conn.commit()
#        print("База данных и таблицы успешно созданы и заполнены тестовыми данными.")
#
#if __name__ == "__main__":
#    create_database()
#
#
#
#
#
#import sqlite3
#import tkinter as tk
#from tkinter import messagebox
#import subprocess
#
#def db_query(query, params=(), fetch=False):
#    with sqlite3.connect("company.db") as conn:
#        conn.execute("PRAGMA foreign_keys = ON")
#        cursor = conn.cursor()
#        cursor.execute(query, params)
#        return cursor.fetchone() if fetch else conn.commit()
#
#def login():
#    user = db_query("SELECT role FROM users WHERE login = ? AND password = ?",
#                    (login_entry.get(), pass_entry.get()), fetch=True)
#    if user:
#        messagebox.showinfo("Успешно", f"Добро пожаловать! Роль: {user[0]}")
#        subprocess.Popen(["python", "dashboard.py"])
#        root.destroy()
#    else:
#        messagebox.showerror("Ошибка", "Неверный логин или пароль")
#
#def register():
#    login_text = login_entry.get()
#    password_text = pass_entry.get()
#    if not login_text or not password_text:
#        return messagebox.showwarning("Ошибка", "Заполните оба поля")
#    if len(password_text) < 8:
#        return messagebox.showwarning("Ошибка", "Пароль должен быть минимум 8 символов")
#    try:
#        db_query("INSERT INTO users (login, password, role) VALUES (?, ?, 'user')",
#                 (login_text, password_text))
#        messagebox.showinfo("Успешно", "Регистрация завершена")
#    except sqlite3.IntegrityError:
#        messagebox.showerror("Ошибка", "Логин уже существует")
#
#def reset_password():
#    login_text = login_entry.get()
#    password_text = pass_entry.get()
#    if not login_text or not password_text:
#        return messagebox.showwarning("Ошибка", "Заполните оба поля")
#    if len(password_text) < 8:
#        return messagebox.showwarning("Ошибка", "Пароль должен быть минимум 8 символов")
#    user = db_query("SELECT 1 FROM users WHERE login = ?", (login_text,), fetch=True)
#    if user:
#        db_query("UPDATE users SET password = ? WHERE login = ?",
#                 (password_text, login_text))
#        messagebox.showinfo("Успешно", "Пароль обновлён")
#    else:
#        messagebox.showerror("Ошибка", "Пользователь не найден")
#
## Интерфейс
#root = tk.Tk()
#root.title("Авторизация")
#root.geometry("300x250")
#
#for text, var in [("Логин:", None), ("Пароль:", "*")]:
#    tk.Label(root, text=text).pack()
#    e = tk.Entry(root, show=var) if var else tk.Entry(root)
#    e.pack()
#    if not var: login_entry = e
#    else: pass_entry = e
#
#for text, cmd in [("Войти", login), ("Регистрация", register), ("Сброс пароля", reset_password)]:
#    tk.Button(root, text=text, command=cmd).pack(pady=5)
#
#root.mainloop()
#
#
#
#
#
#import tkinter as tk
#from tkinter import ttk, simpledialog, messagebox
#import sqlite3
#
#db = "company.db"
#
#def get_cols(t):
#    return [c[1] for c in sqlite3.connect(db).execute(f"PRAGMA table_info({t})")]
#
#def load():
#    t = table.get()
#    cols = get_cols(t)
#    tree.config(columns=cols, show="headings")
#    for c in cols: tree.heading(c, text=c)
#    for i in tree.get_children(): tree.delete(i)
#    for r in sqlite3.connect(db).execute(f"SELECT * FROM {t}"): tree.insert("", "end", values=r)
#
#def edit(e):
#    i, c = tree.focus(), tree.identify_column(e.x)
#    if not i: return
#    col, idx = tree["columns"][int(c[1:])-1], int(c[1:])-1
#    x, y, w, h = tree.bbox(i, c)
#    old = tree.item(i)["values"]
#    ent = tk.Entry(tree); ent.insert(0, old[idx]); ent.place(x=x, y=y, w=w, h=h); ent.focus()
#
#    def save(_):
#        val = ent.get(); ent.destroy()
#        new = list(old); new[idx] = val; tree.item(i, values=new)
#        with sqlite3.connect(db) as conn:
#            conn.execute(f"UPDATE {table.get()} SET {col}=? WHERE id=?", (val, old[0]))
#            conn.commit()
#
#    ent.bind("<Return>", save)
#    ent.bind("<FocusOut>", lambda _: ent.destroy())
#
#def add():
#    t, cols = table.get(), get_cols(table.get())[1:]
#    vals = [simpledialog.askstring("Добавить", f"{c}:") for c in cols]
#    if None in vals: return
#    with sqlite3.connect(db) as conn:
#        conn.execute(f"INSERT INTO {t} ({','.join(cols)}) VALUES ({','.join('?'*len(vals))})", vals)
#        conn.commit()
#    load()
#
#def delete():
#    i = tree.focus()
#    if not i: return
#    row = tree.item(i)["values"]
#    with sqlite3.connect(db) as conn:
#        conn.execute(f"DELETE FROM {table.get()} WHERE id=?", (row[0],))
#        conn.commit()
#    tree.delete(i)
#
#root = tk.Tk(); root.title("SQLite GUI"); root.geometry("700x400")
#table = tk.StringVar(value="users")
#ttk.Combobox(root, textvariable=table, values=["users", "departments", "employees"]).pack()
#f = tk.Frame(root); f.pack()
#tk.Button(f, text="Загрузить", command=load).pack(side="left")
#tk.Button(f, text="Добавить", command=add).pack(side="left")
#tk.Button(f, text="Удалить", command=delete).pack(side="left")
#tree = ttk.Treeview(root); tree.pack(fill="both", expand=True); tree.bind("<Double-1>", edit)
#root.mainloop()