from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
from logging_config import logger
import atexit
import uuid
from flask import render_template, request
from translations import ERROR_MESSAGES

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.errorhandler(404)
def not_found_error(e):
    lang = 'uk'  # можна автоматизувати через headers
    msg = ERROR_MESSAGES[lang][404]
    return render_template('errors/404.html', **msg), 404

@app.errorhandler(500)
def internal_error(e):
    lang = 'uk'
    msg = ERROR_MESSAGES[lang][500]
    return render_template('errors/500.html', **msg), 500

@app.errorhandler(Exception)
def handle_exception(e):
    error_id = str(uuid.uuid4())
    logger.exception(f" Unhandled exception [{error_id}]")

    return render_template("error.html", error_id=error_id), 500

@app.route('/report_issue', methods=['POST'])
def report_issue():
    page = request.form['page']
    details = request.form['details']
    logger.warning(f"Користувач повідомив про проблему на {page}: {details}")
    flash("Дякуємо! Ми отримали ваше повідомлення.", "success")
    return redirect(url_for('home'))

# Параметри підключення до PostgreSQL
db_config = {
    'host': 'localhost',
    'port': '5433',
    'dbname': 'postgres',
    'user': 'postgres',
    'password': '12345'
}


def get_db_connection():
    """
    Створює нове з'єднання з базою даних PostgreSQL.

    Returns:
        connection: Об'єкт з'єднання psycopg2 з базою даних.
    """
    return psycopg2.connect(**db_config)


@app.route('/')
def home():
    """
    Відображає головну сторінку застосунку.

    Returns:
        str: HTML-шаблон головної сторінки.
    """
    return render_template('home.html')


@app.route('/register')
def index():
    """
    Відображає форму реєстрації користувача.

    Returns:
        str: HTML-шаблон сторінки реєстрації.
    """
    return render_template('register.html')


@app.route('/login')
def login():
    """
    Відображає форму логіну користувача.

    Returns:
        str: HTML-шаблон сторінки входу.
    """
    return render_template('login.html')


@app.route('/inventory', methods=['GET', 'POST'])
def inventory():
    """
    Відображає інвентар користувача.

    Якщо користувач не авторизований — перенаправляє на логін.
    Підтягує всі предмети користувача або фільтрує їх за рідкістю.

    Returns:
        str: HTML-сторінка з інвентарем.
    """
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    category_filter = request.form.get('category_filter', None)

    conn = get_db_connection()
    with conn.cursor() as cursor:
        if category_filter:
            cursor.execute(
                'SELECT item_name, rarity, damage, fire_rate FROM inventory WHERE user_id = %s AND rarity = %s',
                (user_id, category_filter)
            )
        else:
            cursor.execute(
                'SELECT item_name, rarity, damage, fire_rate FROM inventory WHERE user_id = %s',
                (user_id,)
            )
        items = cursor.fetchall()

    conn.close()
    return render_template('inventory.html', items=items, selected_category=category_filter)


@app.route('/register', methods=['POST'])
def register():
    """
    Обробляє дані з форми реєстрації.

    Перевіряє, чи співпадають паролі, хешує пароль, перевіряє чи вже існує користувач,
    додає нового користувача в базу даних.

    Returns:
        Response: Редірект на сторінку логіну або інвентарю.
    """
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm-password']

    if password != confirm_password:
        flash("Паролі не співпадають", 'error')
        return redirect(url_for('index'))

    hashed_password = generate_password_hash(password)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
    user = cursor.fetchone()

    if user:
        flash("Цей email вже зареєстрований", 'error')
        conn.close()
        return redirect(url_for('login'))

    cursor.execute(
        'INSERT INTO users (email, password) VALUES (%s, %s)',
        (email, hashed_password)
    )
    conn.commit()
    conn.close()
    return redirect(url_for('inventory'))


@app.route('/login_user', methods=['POST'])
def login_user():
    """
    Обробляє логін користувача.

    Перевіряє правильність email і пароля, зберігає user_id в сесії.

    Returns:
        Response: Редірект на сторінку інвентарю або логіну при помилці.
    """
    email = request.form['email']
    password = request.form['password']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
    user = cursor.fetchone()

    if not user or not check_password_hash(user[2], password):  # user[2] — пароль з бази
        flash("Невірний email або пароль", 'error')
        conn.close()
        return redirect(url_for('login'))

    session['user_id'] = user[0]  # Зберігаємо user_id у сесії
    conn.close()
    return redirect(url_for('inventory'))


@app.route('/logout')
def logout():
    """
    Вихід з облікового запису.

    Видаляє user_id з сесії та перенаправляє на логін.

    Returns:
        Response: Редірект на сторінку логіну.
    """
    session.pop('user_id', None)
    return redirect(url_for('login'))


import uuid
from flask import flash, redirect, render_template, request, url_for, session
import logging

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    """
    Додає новий предмет до інвентарю користувача.

    Якщо користувач не авторизований — перенаправляє на логін.
    У разі POST-запиту — зберігає предмет до бази даних.

    Returns:
        str | Response: HTML-форма або редірект на інвентар.
    """
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        item_name = request.form['item_name']
        rarity = request.form['rarity']
        damage = request.form['damage']
        fire_rate = request.form['fire_rate']
        user_id = session['user_id']

        # Перевірка на порожні поля
        if not item_name or not rarity or not damage or not fire_rate:
            flash(" Усі поля повинні бути заповнені.", "error")
            return render_template('add_item.html')

        try:
            # З'єднання з базою даних
            conn = get_db_connection()
            cursor = conn.cursor()

            # Вставка нового предмета
            cursor.execute(
                'INSERT INTO inventory (item_name, rarity, damage, fire_rate, user_id) VALUES (%s, %s, %s, %s, %s)',
                (item_name, rarity, damage, fire_rate, user_id)
            )
            conn.commit()
            conn.close()

            flash(" Предмет успішно додано до інвентарю!", "success")
            return redirect(url_for('inventory'))

        except Exception as e:
            # Генерація унікального ідентифікатора помилки
            error_id = str(uuid.uuid4())

            # Логування помилки
            logger.exception(f" Помилка при додаванні предмета [{error_id}] | user_id={user_id} | item={item_name} | error={str(e)}")

            # Відправка повідомлення користувачу
            flash(f" Сталася помилка при додаванні предмета. Код помилки: {error_id}", "error")
            return redirect(url_for('add_item'))

    return render_template('add_item.html')


def on_shutdown():
    logger.info("Application stopped")

atexit.register(on_shutdown)

if __name__ == '__main__':
    logger.info("Application started")
    app.run(debug=True, host='0.0.0.0', port=5000)
