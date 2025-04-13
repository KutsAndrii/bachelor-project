Підготовка до оновлення
Перевірити changelog
Повідомити користувачів (якщо можливий downtime)

🛡 Створення резервних копій
pg_dump -U postgres -p 5433 -d postgres -f backup_$(date +%F).sql
cp -r bachelor-project bachelor-project-backup-$(date +%F)

✅ Перевірка сумісності
Перевірити залежності в requirements.txt
Запустити тестовий сервер (локально або staging)

🕒 Планування часу простою (якщо потрібно)
Узгодити з користувачами/адміністрацією (якщо реліз критичний)

🔁 Процес оновлення
Зупинка служб:
sudo systemctl stop app.service

Оновлення коду:
cd bachelor-project
git pull origin main

Міграція БД (якщо є нові таблиці):
psql -U postgres -p 5433 -d postgres -f migrations/add_columns.sql

Оновлення конфігурацій (якщо є):
Перевірити .env, systemd 

Перезапуск служби:
sudo systemctl start app.service

✅ Перевірка після оновлення

Пройти основний функціонал: логін, реєстрація, робота з інвентарем

Перевірити логи:
journalctl -u app.service -f