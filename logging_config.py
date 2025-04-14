import os
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from flask import has_request_context, request, session

os.makedirs("logs", exist_ok=True)

LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG").upper()

class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
            record.user_id = session.get('user_id', 'Anonymous')
        else:
            record.url = None
            record.remote_addr = None
            record.user_id = 'System'
        return super().format(record)

# Формат з контекстом
formatter = RequestFormatter(
    '%(asctime)s - %(levelname)s - %(module)s - [User: %(user_id)s] [IP: %(remote_addr)s] [URL: %(url)s] - %(message)s'
)

logger = logging.getLogger("server_monitoring")
logger.setLevel(getattr(logging, LOG_LEVEL, logging.DEBUG))
logger.propagate = False  # Щоб не дублювались логи у Flask

# Очистити старі хендлери (при перезапуску сервера)
if logger.hasHandlers():
    logger.handlers.clear()

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# File handler з ротацією за розміром
file_handler = RotatingFileHandler("logs/app_size.log", maxBytes=500_000, backupCount=3)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# File handler з ротацією за часом (раз на добу)
time_handler = TimedRotatingFileHandler("logs/app_time.log", when="midnight", interval=1, backupCount=7)
time_handler.setFormatter(formatter)
logger.addHandler(time_handler)
