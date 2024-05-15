import os
import sys
from loguru import logger

# from utils import config_mng

def setup_logger(ini_dict):
    LOG_FILE_PATH = ini_dict['LOGS']['LOG_FILE_PATH']
    LOG_FILE_NAME = ini_dict['LOGS']['LOG_FILE_NAME']
    LOG_LEVEL = ini_dict['LOGS']['LOG_LEVEL']

    os.makedirs(LOG_FILE_PATH, exist_ok=True)
    full_log_path = os.path.join(LOG_FILE_PATH, LOG_FILE_NAME)

    # log format settings
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <5}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )

    logger.remove()
    logger.add(full_log_path, rotation='10 MB', retention='10 days', level=LOG_LEVEL, format=log_format)
    logger.add(sys.stderr, level=LOG_LEVEL, format=log_format)

    return logger
