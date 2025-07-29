import multiprocessing
import logging

logger = logging.getLogger(__name__)

def get_cpu_count():
    count = multiprocessing.cpu_count()
    return count