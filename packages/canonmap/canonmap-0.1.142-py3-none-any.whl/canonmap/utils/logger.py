# canonmap/utils/logger.py

import logging
import sys
from typing import Dict

# will hold all of our named loggers
_loggers: Dict[str, logging.Logger] = {}

def get_logger(name: str) -> logging.Logger:
    """
    Return a module‐scoped logger that:
     - has its own StreamHandler writing to stdout
     - does NOT propagate to root (so we control exactly when it prints)
     - defaults to WARNING, NOT INFO
    """
    full_name = f"canonmap.{name}"
    if full_name in _loggers:
        return _loggers[full_name]

    logger = logging.getLogger(full_name)
    logger.setLevel(logging.WARNING)
    logger.propagate = False

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.NOTSET)   # let the logger’s level do the filtering
    fmt = "%(asctime)s %(name)s %(levelname)s │ %(message)s"
    handler.setFormatter(logging.Formatter(fmt, datefmt="%Y-%m-%d %H:%M:%S"))
    logger.addHandler(handler)

    _loggers[full_name] = logger
    return logger