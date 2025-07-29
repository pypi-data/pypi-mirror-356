# canonmap/utils/logger.py

import logging
import sys
from typing import Optional, Dict

class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG':    '\033[94m🐛 DEBUG\033[0m',
        'INFO':     '\033[92mℹ️  INFO\033[0m',
        'WARNING':  '\033[93m⚠️  WARNING\033[0m',
        'ERROR':    '\033[91m❌ ERROR\033[0m',
        'CRITICAL': '\033[95m🔥 CRITICAL\033[0m'
    }

    def format(self, record: logging.LogRecord) -> str:
        levelname = self.COLORS.get(record.levelname, record.levelname)
        message = super().format(record)
        return f"{levelname} | {message}"


# keep one configured logger per name
_loggers: Dict[str, logging.Logger] = {}


def get_logger(name: str = "canonmap") -> logging.Logger:
    """
    Get a logger with the given name, configured with our ColoredFormatter.
    Subsequent calls with the same name return the same instance.
    """
    if name in _loggers:
        return _loggers[name]

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        fmt = '%(asctime)s | %(name)s | %(message)s'
        formatter = ColoredFormatter(fmt, datefmt='%Y-%m-%d %H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # quiet down some noisy third-party loggers
        logging.getLogger("sentence_transformers").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        logging.getLogger("transformers").setLevel(logging.WARNING)

    _loggers[name] = logger
    return logger


def set_logger(logger: Optional[logging.Logger] = None) -> logging.Logger:
    """
    Replace or reset the logger for its own name.
    If you pass in a pre-configured logger, it will be used as is.
    Otherwise returns the default 'canonmap' logger.
    """
    if logger is not None:
        _loggers[logger.name] = logger
        return logger
    return get_logger()