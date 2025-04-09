from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Параметри підключення до PostgreSQL
db_config = {
    'host': 'localhost',
    'port': '5433',
    'dbname': 'postgres',
    'user': 'postgres',
    'password': '12345'
}

# Функція для створення з'єднання з базою даних
def get_db_connection():
    return psycopg2.connect(**db_config)

# Головна сторінка - Форма реєстрації
@app.route('/')
def index():
    return render_template('register.html')

# Сторінка логіну
@app.route('/login')
def login():
    return render_template('login.html')

# Сторінка інвентарю
@app.route('/inventory', methods=['GET', 'POST'])
def inventory():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    category_filter = request.form.get('category_filter', None)

    conn = get_db_connection()
    with conn.cursor() as cursor:
        if category_filter:
            cursor.execute('SELECT item_name, rarity, damage, fire_rate FROM inventory WHERE user_id = %s AND rarity = %s', (user_id, category_filter))
        else:
            cursor.execute('SELECT item_name, rarity, damage, fire_rate FROM inventory WHERE user_id = %s', (user_id,))
        
        items = cursor.fetchall()

    conn.close()

    return render_template('inventory.html', items=items, selected_category=category_filter)


# Обробка даних реєстрації
@app.route('/register', methods=['POST'])
def register():
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

    cursor.execute('INSERT INTO users (email, password) VALUES (%s, %s)', (email, hashed_password))
    conn.commit()
    conn.close()
    return redirect(url_for('inventory'))

# Обробка даних логіну
@app.route('/login_user', methods=['POST'])
def login_user():
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

# Обробка виходу з облікового запису
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

# Сторінка для додавання предмета
@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        item_name = request.form['item_name']
        rarity = request.form['rarity']
        damage = request.form['damage']
        fire_rate = request.form['fire_rate']
        user_id = session['user_id']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO inventory (item_name, rarity, damage, fire_rate, user_id) VALUES (%s, %s, %s, %s, %s)',
            (item_name, rarity, damage, fire_rate, user_id)
        )
        conn.commit()
        conn.close()

       
        return redirect(url_for('inventory'))
    
    return render_template('add_item.html')

if __name__ == '__main__':
      app.run(debug=True, host='0.0.0.0', port=5000)
