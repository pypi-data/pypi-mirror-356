# canonmap/utils/logger.py

import logging
import sys
from typing import Optional, Dict

class ColoredFormatter(logging.Formatter):
    # ANSI-colours for levels
    LEVEL_COLORS = {
        'DEBUG':    '\033[94m🐛 DEBUG\033[0m',
        'INFO':     '\033[92mℹ️  INFO\033[0m',
        'WARNING':  '\033[93m⚠️  WARNING\033[0m',
        'ERROR':    '\033[91m❌ ERROR\033[0m',
        'CRITICAL': '\033[95m🔥 CRITICAL\033[0m'
    }
    # ANSI-colour for the logger name (cyan)
    NAME_COLOR = '\033[96m{}\033[0m'

    def __init__(self, fmt: str, datefmt: Optional[str] = None):
        super().__init__(fmt, datefmt=datefmt)

    def format(self, record: logging.LogRecord) -> str:
        # Color the level
        levelname_colored = self.LEVEL_COLORS.get(record.levelname, record.levelname)

        # Temporarily colour the logger name
        original_name = record.name
        record.name = self.NAME_COLOR.format(original_name)

        # Let the base formatter build the timestamp + name + message
        message = super().format(record)

        # Restore the original name so we don't break anything else
        record.name = original_name

        # Prepend the coloured level to the rest
        return f"{levelname_colored} | {message}"


# keep one logger instance per name
_loggers: Dict[str, logging.Logger] = {}

def get_logger(name: str = "canonmap") -> logging.Logger:
    """
    Get (or create) a logger with the given name,
    configured with our ColoredFormatter.
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

        # quiet down a few noisy libraries
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