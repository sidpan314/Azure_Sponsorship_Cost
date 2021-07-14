import logging
import os


class LoggingFormatter(logging.Formatter):
    """Logging Formatter to add colors and count warning / errors"""

    blue = "\033[94m"
    yellow = "\033[93m"
    green = "\033[92m"
    red = "\033[91m"
    bold_red = "\033[31m"
    reset = "\033[0m"
    if os.environ.get("CANALYYZER_LOG_EXPLICIT"):
        format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    else:
        format = "[%(levelname)s] [%(name)s] %(asctime)s - %(message)s"

    FORMATS = {
        logging.DEBUG: blue + format + reset,
        logging.INFO: green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
