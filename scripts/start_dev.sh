#!/bin/bash

echo "[DEV] Стартуємо додаток у режимі розробки..."
export FLASK_APP=app.py
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=5000
