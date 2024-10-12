import time
import logging
from contextlib import contextmanager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def profile_time(func):
    """Decorator to profile the execution time of a function."""
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        logging.info(f"Function '{func.__name__}' took {end_time - start_time:.4f} seconds")
        return result
    return wrapper

@contextmanager
def profile_block():
    """Context manager to profile the execution time of a block of code."""
    start_time = time.perf_counter()
    yield
    end_time = time.perf_counter()
    logging.info(f"Code block took {end_time - start_time:.4f} seconds")

@contextmanager
def profile_line():
    """Context manager to profile the execution time of specific lines of code."""
    start_time = time.perf_counter()
    yield
    end_time = time.perf_counter()
    logging.info(f"Line(s) took {end_time - start_time:.4f} seconds")
