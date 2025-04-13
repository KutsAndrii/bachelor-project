#!/bin/bash

echo "[PROD] Запускаємо додаток з Gunicorn..."

# Запуск Gunicorn з 4-ма воркерами
gunicorn app:app \
  --bind 0.0.0.0:8000 \
  --workers 4 \
  --log-level info \
  --access-logfile logs/access.log \
  --error-logfile logs/error.log
