# canonmap/utils/logger.py

import logging
import sys
from typing import Dict, Optional

class ColoredFormatter(logging.Formatter):
    # ANSI colors + emojis for levels
    LEVEL_COLORS = {
        'DEBUG':    '\033[94m🐛 DEBUG\033[0m',
        'INFO':     '\033[92mℹ️  INFO\033[0m',
        'WARNING':  '\033[93m⚠️  WARNING\033[0m',
        'ERROR':    '\033[91m❌ ERROR\033[0m',
        'CRITICAL': '\033[95m🔥 CRITICAL\033[0m',
    }
    NAME_COLOR = '\033[96m{}\033[0m'

    def __init__(self, fmt: str, datefmt: Optional[str] = None):
        super().__init__(fmt, datefmt=datefmt)

    def format(self, record: logging.LogRecord) -> str:
        # 1) Color the level name
        levelname_colored = self.LEVEL_COLORS.get(record.levelname, record.levelname)

        # 2) Temporarily color the logger name
        original_name = record.name
        record.name = self.NAME_COLOR.format(original_name)

        # 3) Base formatted message (timestamp | name | message)
        base = super().format(record)

        # 4) Restore original
        record.name = original_name

        # 5) Prepend the colored level indicator
        return f"{levelname_colored} | {base}"


# one logger instance per canonical name
_loggers: Dict[str, logging.Logger] = {}


def get_logger(name: str) -> logging.Logger:
    """
    Return a module-scoped logger under 'canonmap.{name}' that:
     - uses our ColoredFormatter
     - defaults to WARNING (so nothing prints until you explicitly raise it)
     - does NOT propagate to the root logger (avoiding duplicates)
    """
    full_name = f"canonmap.{name}"
    if full_name in _loggers:
        return _loggers[full_name]

    logger = logging.getLogger(full_name)
    logger.setLevel(logging.WARNING)
    logger.propagate = False

    # Add our single StreamHandler if none exist
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.NOTSET)  # routing is controlled by logger.level
        fmt = "%(asctime)s | %(name)s | %(message)s"
        handler.setFormatter(ColoredFormatter(fmt, datefmt="%Y-%m-%d %H:%M:%S"))
        logger.addHandler(handler)

    # Silence overly-chatty 3rd-party modules at WARNING
    for noisy in ("sentence_transformers", "urllib3", "transformers"):
        logging.getLogger(noisy).setLevel(logging.WARNING)

    _loggers[full_name] = logger
    return logger


def set_logger(logger: Optional[logging.Logger] = None) -> logging.Logger:
    """
    Replace or reset the logger for its own name.
    If you pass in a fully-configured Logger, we'll store and return that.
    Otherwise returns the default 'canonmap' logger.
    """
    if logger is not None:
        _loggers[logger.name] = logger
        return logger
    return get_logger("canonmap")