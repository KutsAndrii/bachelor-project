# logging_config.py

import os
import logging
from logging.handlers import RotatingFileHandler

LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG").upper()

logger = logging.getLogger("server_monitoring")
logger.setLevel(getattr(logging, LOG_LEVEL, logging.DEBUG))

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s')

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# File handler with rotation
file_handler = RotatingFileHandler("app.log", maxBytes=1000000, backupCount=5)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
