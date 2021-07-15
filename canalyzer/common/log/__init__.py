import os
import logging
from canalyzer.common.log.logging_formatter import LoggingFormatter

logger = logging.getLogger("canalyzer")


def get_log_level():
    log_level_var = os.environ.get("CANALYZER_LOG_LEVEL", "DEBUG").lower()
    log_level = logging.DEBUG
    if log_level_var == "info":
        log_level = logging.INFO
    elif log_level_var == "debug":
        log_level = logging.DEBUG
    elif log_level_var == "warn" or log_level_var == "warning":
        log_level = logging.WARNING
    elif log_level_var == "error":
        log_level = logging.ERROR
    elif log_level_var == "fatal":
        log_level = logging.FATAL
    return log_level


def set_handler(logger):
    log_level = get_log_level()
    logger.setLevel(log_level)
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    ch.setFormatter(LoggingFormatter())

    logger.addHandler(ch)


set_handler(logger)
