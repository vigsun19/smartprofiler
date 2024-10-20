import tracemalloc
import threading
import logging
import functools
from contextlib import contextmanager

# Thread-local storage to handle per-thread profiling data
_thread_local = threading.local()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def profile_memory(func):
    """Decorator to profile the memory usage of a function using tracemalloc."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        tracemalloc.start()  # Start memory tracking
        try:
            result = func(*args, **kwargs)
        finally:
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()  # Stop memory tracking
            logging.info(f"Function '{func.__name__}' used {peak / 1024:.2f} KB of memory (peak)")
        return result
    return wrapper

@contextmanager
def profile_block(profile_type='memory'):
    """Context manager to profile a block of code (memory)."""
    if profile_type == 'memory':
        tracemalloc.start()
        try:
            yield
        finally:
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            logging.info(f"Code block used {peak / 1024:.2f} KB of memory (peak)")
    else:
        logging.error(f"Unknown profile_type: '{profile_type}', use 'memory'")
        raise ValueError(f"Unknown profile_type: '{profile_type}', use 'memory'")

@contextmanager
def profile_line(profile_type='memory'):
    """Context manager to profile specific lines of code (memory)."""
    if profile_type == 'memory':
        tracemalloc.start()
        try:
            yield
        finally:
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            logging.info(f"Line(s) used {peak / 1024:.2f} KB of memory (peak)")
    else:
        logging.error(f"Unknown profile_type: '{profile_type}', use 'memory'")
        raise ValueError(f"Unknown profile_type: '{profile_type}', use 'memory'")
