README.txt

Назва проєкту:
Веб-застосунок для управління інвентарем користувача

Опис:
Цей веб-додаток створений у межах бакалаврської роботи. Він дозволяє користувачам реєструватися, входити в систему, додавати, переглядати та фільтрувати предмети інвентарю. Інтерфейс створений за допомогою HTML, CSS, а валідація форм реалізована через JavaScript. На серверній стороні використовується Flask (Python) та PostgreSQL як СУБД.

Використані технології:

Back-end:
- Python 3.x
- Flask
- psycopg2
- Werkzeug (хешування паролів)

Front-end:
- HTML
- CSS
- JavaScript
  * validation.js – перевірка полів реєстрації
  * validation_login.js – перевірка полів авторизації
  * validation_modal.js - скрипт для модального вікна

База даних:
- PostgreSQL

Передумови для запуску:

1. Встановлений Python 3.6 або новіший
2. Встановлений PostgreSQL (порт: 5433)
3. Необхідні бібліотеки встановлюються командою:
   pip install flask psycopg2 werkzeug

Структура бази даних:

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE inventory (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(255) NOT NULL,
    rarity VARCHAR(50),
    damage INTEGER,
    fire_rate INTEGER,
    user_id INTEGER REFERENCES users(id)
);

Функціональність додатку:

- Реєстрація користувачів з перевіркою правильності введення
- Авторизація користувачів
- Перегляд списку предметів інвентарю
- Фільтрація інвентарю за рідкістю
- Додавання нових предметів до інвентарю
- Вихід із системи
- Захист через хешування паролів і перевірку сесій

Інструкція з запуску:

1. Відредагуйте параметри підключення до бази даних у коді app.py:

   db_config = {
       'host': 'localhost',
       'port': '5433',
       'dbname': 'postgres',
       'user': 'postgres',
       'password': '12345'
   }

2. Запустіть додаток командою:
   python app.py

3. Відкрийте браузер і перейдіть за адресою:
   http://localhost:5000/

Автор:
[Куц Андрій]
[ЕлІТ, Інформатика]
[Сумський державний університет]
[2025]
