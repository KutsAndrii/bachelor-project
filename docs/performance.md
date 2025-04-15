# Профілювання продуктивності додавання елементів

Цей документ описує методологію профілювання продуктивності для додавання елементів у додаток та базу даних. Ми використовували Python профілювальник `memory_profiler` для вимірювання споживаної пам'яті, а також для оцінки часу виконання запитів до бази даних.

## Профілювання додавання елемента

Запит на додавання елемента був виконаний через HTTP POST запит до сервера. Ось результати профілювання:

**Файл**: `D:\QA1\tests\perf_scenarios.py`

```plaintext
Line #    Mem usage    Increment  Occurrences   Line Contents
=============================================================
    20     50.9 MiB     50.9 MiB           1   @profile
    21                                         def test_add_item():
    22     50.9 MiB      0.0 MiB           1       url = "http://127.0.0.1:5000/add_item"
    23     50.9 MiB      0.0 MiB           1       data = {"name": "test_item", "description": "Test item description"}
    24
    25     51.2 MiB      0.3 MiB           1       response = requests.post(url, json=data)
    26     51.2 MiB      0.0 MiB           1       print(f"Status: {response.status_code}")
    27     51.2 MiB      0.0 MiB           1       return response

Висновок:
Виконання запиту на додавання елемента займає мінімальний час, з незначними витратами пам'яті.
Пам'ять після виконання запиту збільшилася на 0.3 Мб.

Профілювання додавання елемента до БД
Наступним кроком було профілювання запиту до бази даних для додавання елементів. Ось результати профілювання:

Файл: D:\QA1\tests\perf_scenarios.py

Line #    Mem usage    Increment  Occurrences   Line Contents
=============================================================
    30     52.2 MiB     52.2 MiB           1   @profile
    31                                         def execute_query(query, data=None):
    32     52.2 MiB      0.0 MiB           1       start_time = time()
    33
    34     53.3 MiB      1.1 MiB           1       conn = get_db_connection()      
    35     53.3 MiB      0.0 MiB           1       cursor = conn.cursor()
    36
    37     53.3 MiB      0.0 MiB           1       if data:
    38                                                 # Перевірка: якщо data — список кортежів (масова вставка)
    39     53.3 MiB      0.0 MiB           1           if isinstance(data, list) and isinstance(data[0], tuple):
    40     53.3 MiB      0.0 MiB           1               cursor.executemany(query, data)
    41                                                 else:
    42                                                     cursor.execute(query, data)
    43                                             else:
    44                                                 cursor.execute(query)
    45
    46     53.3 MiB      0.0 MiB           1       if query.strip().upper().startswith("SELECT"):
    47                                                 results = cursor.fetchall()
    48                                                 print(f"Результати запиту: {results}")
    49
    50     53.3 MiB      0.0 MiB           1       conn.commit()
    51     53.3 MiB      0.0 MiB           1       execution_time = time() - start_time
    52     53.3 MiB      0.0 MiB           1       print(f"Запит виконано за {execution_time:.4f} сек.")
    53
    54     53.3 MiB      0.0 MiB           1       cursor.close()
    55     53.3 MiB      0.0 MiB           1       conn.close()

Висновок:
Запит до бази даних виконується швидко (0.1323 сек.), з невеликим збільшенням споживаної пам'яті (1.1 Мб).

Основний час витрачається на створення з'єднання з базою даних та виконання запиту.

Додавання 1000 елементів до БД
Було протестовано додавання 1000 елементів до бази даних. Ось результати профілювання:

Файл: D:\QA1\tests\perf_scenarios.py

Line #    Mem usage    Increment  Occurrences   Line Contents
=============================================================
    60     52.2 MiB     52.2 MiB           1   @profile
    61                                         def test_add_item_to_db():
    62     52.2 MiB      0.0 MiB           1       query = """
    63                                             INSERT INTO inventory (user_id, item_name, rarity, damage, fire_rate)
    64                                             VALUES (%s, %s, %s, %s, %s)
    65                                             """
    66
    67     52.2 MiB      0.0 MiB           1       items = []
    68     52.2 MiB      0.0 MiB        1001       for i in range(1000):
    69     52.2 MiB      0.0 MiB        2000           items.append((
    70     52.2 MiB      0.0 MiB        1000               1,
    71     52.2 MiB      0.0 MiB        1000               f"test_item_{i}",
    72     52.2 MiB      0.0 MiB        1000               "Epic",
    73     52.2 MiB      0.0 MiB        1000               100 + i % 50,
    74     52.2 MiB      0.0 MiB        1000               round(1.0 + (i % 10) * 0.5, 2)
    75                                                 ))
    76
    77     53.3 MiB      1.1 MiB           1       execute_query(query, items)
    78     53.3 MiB      0.0 MiB           1       print("Додано 1000 предметів.")

Висновок:
Додавання 1000 елементів до бази даних виконується з витратою пам'яті 1.1 Мб.

Кількість елементів у базі даних значно зросла, і це показує ефективність вставки в масив.

Профілювання отримання елементів з БД
Виконано профілювання запиту для отримання елементів з бази даних. Ось результат:
Результати запиту: [(1017, 1, 'test_item_0', 'Epic', 100, Decimal('1.0'), datetime.datetime(2025, 4, 15, 14, 30, 50, 909011)), ...]
Висновок:
Час виконання запиту на отримання елементів з бази даних становить кілька мілісекунд.
Результати запиту демонструють наявність елементів з різними характеристиками.