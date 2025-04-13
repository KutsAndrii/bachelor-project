@echo off
echo [DEV] Запуск Flask-додатку у режимі розробки...
set FLASK_APP=app.py
set FLASK_ENV=development
flask run --host=0.0.0.0 --port=5000
pause
