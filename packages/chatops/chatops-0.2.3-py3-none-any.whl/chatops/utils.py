from functools import wraps
from time import perf_counter
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_command(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info("Running %s", func.__name__)
        return func(*args, **kwargs)
    return wrapper


def time_command(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            duration = perf_counter() - start
            logger.info("%s completed in %.2fs", func.__name__, duration)
    return wrapper
