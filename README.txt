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

## 📚 Documentation Guidelines

Цей проєкт використовує стандартизоване документування коду для Python (Flask) та JavaScript.

### 🐍 Python (Flask)

- Формат документації: **Sphinx-style docstrings**
- Документуються всі ключові функції, методи, класи.
- Документація пишеться одразу після сигнатури функції у потрійному лапках `"""`.

#### 📌 Приклад:
```python
def get_user_items(user_id):
    """
    Отримує список предметів для конкретного користувача.

    Args:
        user_id (int): Ідентифікатор користувача.

    Returns:
        list: Список кортежів з даними про предмети.
    """

💻 JavaScript
Формат: JSDoc

Документуються функції, що взаємодіють з DOM, валідацією та логікою.

Коментар розміщується безпосередньо перед функцією у вигляді багаторядкового блоку /** ... */

/**
 * Виводить повідомлення про помилку.
 * @param {HTMLElement} element - Елемент, біля якого показати помилку.
 * @param {string} message - Текст повідомлення про помилку.
 */
function showError(element, message) {
    ...
}

✅ Загальні правила
Усі нові функції мають бути задокументовані.

Якщо змінюється логіка або параметри — оновлюється і документація.

Документація — частина коду. Без неї зміни не приймаються в main.

📘 Інструкція для розробника 
🧠 Ця інструкція призначена для розробника, який має чисту ОС і хоче приєднатись до проєкту.

📌 Крок 1: Встановлення необхідного ПЗ

✅ Встановити Python 3.10+
Завантажити з офіційного сайту: https://www.python.org/downloads/
Під час встановлення обов’язково поставити галочку “Add Python to PATH”

Перевірка:
python --version
pip --version

✅ Встановити Git
Завантажити: https://git-scm.com/downloads

Перевірка:
git --version

✅ Встановити PostgreSQL (версія 14+)
Завантажити: https://www.postgresql.org/download/
Запам’ятати:
порт 5433
логін postgres
пароль 12345

Після встановлення:
Запустити pgAdmin або psql
Створити базу з назвою postgres (якщо ще не існує)

📌 Крок 2: Клонування проєкту
git clone https://github.com/KutsAndrii/bachelor-project.git
cd bachelor-project

📌 Крок 3: Створення віртуального середовища
python -m venv venv

# Windows:
venv\Scripts\activate

# Linux/macOS:
source venv/bin/activate

📌 Крок 4: Встановлення залежностей
pip install -r requirements.txt
pip install flask psycopg2-binary werkzeug
pip freeze > requirements.txt

📌 Крок 5: Імпорт структури БД
Створити таблиці вручну або імпортувати:

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE inventory (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100),
    rarity VARCHAR(50),
    damage INTEGER,
    fire_rate FLOAT,
    user_id INTEGER REFERENCES users(id)
);


Якщо помилка: перевір, чи підключення відповідає конфігурації в app.py (host, port, user, password).

📌 Крок 6: Запуск проєкту у режимі розробки
python app.py
За замовчуванням запускається на http://localhost:5000


Автор:
[Куц Андрій]
[ЕлІТ, Інформатика]
[Сумський державний університет]
[2025]
