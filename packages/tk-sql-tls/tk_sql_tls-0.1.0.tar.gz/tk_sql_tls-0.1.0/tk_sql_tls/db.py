import sqlite3

def create_database():
    with sqlite3.connect("company.db") as conn:
        cursor = conn.cursor()

        # Таблица пользователей
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
        """)

        # Таблица отделов
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT
        )
        """)

        # Таблица сотрудников
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            position TEXT,
            user_id INTEGER,
            department_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (department_id) REFERENCES departments(id)
        )
        """)

        # Добавление тестовых пользователей
        users = [
            ('admin', 'adminpass', 'admin'),
            ('johndoe', 'password123', 'user'),
            ('janedoe', 'securepass', 'user')
        ]
        cursor.executemany("INSERT OR IGNORE INTO users (login, password, role) VALUES (?, ?, ?)", users)

        # Добавление отделов
        departments = [
            ('IT', 'Отдел информационных технологий'),
            ('HR', 'Отдел кадров'),
            ('Sales', 'Отдел продаж')
        ]
        cursor.executemany("INSERT OR IGNORE INTO departments (name, description) VALUES (?, ?)", departments)

        # Получаем id пользователей и отделов для вставки сотрудников
        cursor.execute("SELECT id FROM users WHERE login = 'johndoe'")
        johndoe_id = cursor.fetchone()[0]

        cursor.execute("SELECT id FROM users WHERE login = 'janedoe'")
        janedoe_id = cursor.fetchone()[0]

        cursor.execute("SELECT id FROM departments WHERE name = 'IT'")
        it_dept_id = cursor.fetchone()[0]

        cursor.execute("SELECT id FROM departments WHERE name = 'HR'")
        hr_dept_id = cursor.fetchone()[0]

        # Добавление сотрудников
        employees = [
            ('Джон Доу', 'Программист', johndoe_id, it_dept_id),
            ('Джейн Доу', 'HR-специалист', janedoe_id, hr_dept_id)
        ]
        cursor.executemany("""
            INSERT OR IGNORE INTO employees (full_name, position, user_id, department_id)
            VALUES (?, ?, ?, ?)
        """, employees)

        conn.commit()
        print("База данных и таблицы успешно созданы и заполнены тестовыми данными.")

if __name__ == "__main__":
    create_database()
