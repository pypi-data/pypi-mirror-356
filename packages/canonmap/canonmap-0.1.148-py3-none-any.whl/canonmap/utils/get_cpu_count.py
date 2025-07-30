import multiprocessing

from canonmap.utils.logger import get_logger

logger = get_logger("get_cpu_count")

def get_cpu_count():
    count = multiprocessing.cpu_count()
    return count