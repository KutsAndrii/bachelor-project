Rollback-процедура

⏪ У разі невдалого оновлення

Зупинити проєкт:
sudo systemctl stop app.service

Відновити попередній код:
rm -rf bachelor-project
cp -r bachelor-project-backup-YYYY-MM-DD bachelor-project

Відновити БД:

psql -U postgres -p 5433 -d postgres -f backup_YYYY-MM-DD.sql

Запустити застосунок:
sudo systemctl start app.service

✅ Тепер система повернута до стабільного стану.