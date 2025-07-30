# canonmap/utils/logger.py

import logging
import sys

_loggers: dict[str, logging.Logger] = {}

# ANSI color codes
_COLORS = {
    "DEBUG": "\033[94m",    # blue
    "INFO": "\033[92m",     # green
    "WARNING": "\033[93m",  # yellow
    "ERROR": "\033[91m",    # red
    "RESET": "\033[0m",
}

class _ColorFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        level = record.levelname
        color = _COLORS.get(level, "")
        reset = _COLORS["RESET"]
        icon = {
            "DEBUG": "🐛",
            "INFO": "ℹ️ ",
            "WARNING": "⚠️ ",
            "ERROR": "❌",
            "CRITICAL": "💥",
        }.get(level, "")
        prefix = f"{icon}{color}{level}{reset}"
        msg = super().format(record)
        return f"{prefix} | {record.name} | {msg}"

def get_logger(name: str) -> logging.Logger:
    if name in _loggers:
        return _loggers[name]

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)  # default level
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(_ColorFormatter("%(message)s"))
    logger.addHandler(handler)
    logger.propagate = False
    _loggers[name] = logger
    return logger