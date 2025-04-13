@echo off
echo [PROD] Запуск Flask-додатку з Gunicorn...
REM Gunicorn не працює на Windows, тож це скоріше для WSL або Linux-серверів
REM Можеш використовувати waitress замість gunicorn, якщо дуже треба на Windows

REM Приклад з waitress:
python -m waitress --host=0.0.0.0 --port=8000 app:app

pause
