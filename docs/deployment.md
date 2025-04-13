 Інструкція з розгортання проєкту (Production)

🖥 Вимоги до апаратного забезпечення

Компонент       Мінімум

CPU             2 ядра (x86_64)

RAM             2 GB

SSD/Диск        5 GB (для коду + бази даних)

ОС              Ubuntu 22.04+ / Debian 11+

⚙️ Необхідне програмне забезпечення

Python 3.10+
PostgreSQL 14+
Git
pip / venv


🌐 Налаштування мережі

Відкриті порти:
5000 (для Flask — лише локально або через reverse proxy)
5433 (PostgreSQL, локальний або з обмеженим доступом)

⚙️ Конфігурація серверів

Створити користувача appuser та віртуальне середовище:
sudo adduser appuser
sudo su - appuser
python3 -m venv venv
source venv/bin/activate

Встановити залежності:
pip install -r requirements.txt

Налаштувати app.py 

🗃 Налаштування СУБД PostgreSQL
Переконатися, що сервер PostgreSQL запущено на порту 5433

Створити таблиці (якщо не існують):
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


🚀 Розгортання коду

git clone https://github.com/KutsAndrii/bachelor-project.git
cd your-repo
source venv/bin/activate
pip install -r requirements.txt

Запуск:
python app.py
Або через systemd/supervisor для автозапуску

✅ Перевірка працездатності
Відкрити: http://127.0.0.1:5000

Перевірити:
Рендер головної сторінки
Реєстрація/логін користувача
Робота з базою: додавання предметів до інвентаря