import sqlite3

DATABASE = 'recipebook.db'


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            ingredients TEXT NOT NULL,
            cooking TEXT NOT NULL,
            time INTEGER NOT NULL
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


def reg_user(username, password):
    """
    Регистрация пользователя
    """
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO users (username, password) VALUES (?, ?)', (username, password)
    )
    conn.commit()
    conn.close()


def check_user(username, password):
    """
    Проверяет, существует ли пользователь с таким логином и паролем.
    Возвращает True, если пользователь найден, иначе False.
    """
    conn = get_db_connection()
    user = conn.execute(
        'SELECT * FROM users WHERE username = ? AND password = ?',
        (username, password)
    ).fetchone()
    conn.close()
    return user is not None


def get_all_recipes():
    """
    Вывод всех рецептов
    """
    conn = get_db_connection()
    recipes = conn.execute(
        'SELECT * FROM recipes'
    ).fetchall()
    conn.close()
    return recipes


def get_recipes(item_id):
    conn = get_db_connection()
    recipes = conn.execute(
        'SELECT * FROM recipes WHERE id = ?', (item_id,)
    ).fetchone()
    conn.close()
    return recipes


def add_recipes(name, category, ingredients, cooking, time):
    """
    Добавление рецептов
    """
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO recipes (name, category, ingredients, cooking, time) VALUES (?, ?, ?, ?, ?)',
        (name, category, ingredients, cooking, time)
    )
    conn.commit()
    conn.close()


def update_recipes(name, category, ingredients, cooking, time, item_id):
    """
    Обновление рецептов
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE recipes SET name = ?, category = ?, ingredients = ?, cooking = ?, time = ? WHERE id = ?',
        (name, category, ingredients, cooking, time, item_id)
    )
    conn.commit()

    updated_recipe = cursor.execute(
        'SELECT * FROM recipes WHERE id = ?', (item_id,)
    ).fetchone()

    conn.close()
    return updated_recipe


def delete_recipes(item_id):
    """
    Удаление рецептов
    """
    conn = get_db_connection()
    conn.execute(
        'DELETE FROM recipes WHERE id = ?', (item_id,)
    )
    conn.commit()
    conn.close()


def get_sort_soup():
    """
    Фильтрация супов
    """
    conn = get_db_connection()
    recipes = conn.execute(
        "SELECT * FROM recipes WHERE category = 'супы' ORDER BY name"
    ).fetchall()
    conn.close()
    return recipes


def get_sort_salad():
    """
    Фильтрация салатов
    """
    conn = get_db_connection()
    recipes = conn.execute(
        "SELECT * FROM recipes WHERE category = 'салаты' ORDER BY name"
    ).fetchall()
    conn.close()
    return recipes


def get_sort_desserts():
    """
    Фильтрация десертов
    """
    conn = get_db_connection()
    recipes = conn.execute(
        "SELECT * FROM recipes WHERE category = 'десерты' ORDER BY name"
    ).fetchall()
    conn.close()
    return recipes