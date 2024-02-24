import time
import datetime
import os
from loguru import logger
from API.API_settings import YandexDiskConnector
from config_data.config import token_api, remove_path, local_path


def configure_logger():
    log_file = "log_data.log"
    logger.add(log_file, rotation="10 MB", level="INFO", format="{time} {level} {message}")


