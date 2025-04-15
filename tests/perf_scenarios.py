import psycopg2
from time import time
from memory_profiler import profile
import requests


# Функція для підключення до БД PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        host='localhost',         # хост БД
        port='5433',              # порт PostgreSQL
        dbname='postgres',        # ім'я БД
        user='postgres',          # ім'я користувача
        password='12345'          # пароль користувача
    )
    return conn
   

# Декоратор для моніторингу пам'яті
@profile
def test_add_item():
    url = "http://127.0.0.1:5000/add_item"
    data = {"name": "test_item", "description": "Test item description"}

    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    return response

# Функція для виконання SQL-запиту (приклад з профілюванням)
@profile
def execute_query(query, data=None):
    start_time = time()

    conn = get_db_connection()
    cursor = conn.cursor()

    if data:
        # Перевірка: якщо data — список кортежів (масова вставка)
        if isinstance(data, list) and isinstance(data[0], tuple):
            cursor.executemany(query, data)
        else:
            cursor.execute(query, data)
    else:
        cursor.execute(query)

    if query.strip().upper().startswith("SELECT"):
        results = cursor.fetchall()
        print(f"Результати запиту: {results}")

    conn.commit()
    execution_time = time() - start_time
    print(f"Запит виконано за {execution_time:.4f} сек.")

    cursor.close()
    conn.close()



# Тестова функція для додавання елементів з профілюванням запиту до БД
@profile
def test_add_item_to_db():
    query = """
    INSERT INTO inventory (user_id, item_name, rarity, damage, fire_rate)
    VALUES (%s, %s, %s, %s, %s)
    """

    items = []
    for i in range(1000):
        items.append((
            1,
            f"test_item_{i}",
            "Epic",
            100 + i % 50,
            round(1.0 + (i % 10) * 0.5, 2)
        ))

    execute_query(query, items)
    print("Додано 1000 предметів.")




# Тестова функція для отримання елементів з БД
@profile
def test_list_items_from_db():
    query = "SELECT * FROM inventory LIMIT 100"  # Оновлений запит на отримання елементів з таблиці inventory
    execute_query(query)  # Тепер передаємо тільки запит без data

