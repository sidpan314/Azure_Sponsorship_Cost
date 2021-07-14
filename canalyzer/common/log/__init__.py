import logging
from canalyzer.common.log.logging_formatter import LoggingFormatter

logger = logging.getLogger("canalyzer")
logger.setLevel(logging.DEBUG)


def set_handler(logger):
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(LoggingFormatter())

    logger.addHandler(ch)


set_handler(logger)
