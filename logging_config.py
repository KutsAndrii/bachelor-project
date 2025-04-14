# logging_config.py
import logging

LOG_FORMAT = "%(asctime)s - [%(levelname)s] - %(name)s - %(message)s"

logging.basicConfig(
    level=logging.DEBUG,  # буде змінюватися далі
    format=LOG_FORMAT,
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("server_monitor")
