import time
import tracemalloc
import threading
import logging
from contextlib import contextmanager

# Thread-local storage to handle per-thread profiling data
_thread_local = threading.local()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def profile_time(func):
    """Decorator to profile the execution time of a function."""
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        try:
            result = func(*args, **kwargs)
        finally:
            end_time = time.perf_counter()
            logging.info(f"Function '{func.__name__}' took {end_time - start_time:.4f} seconds")
        return result
    return wrapper

def profile_memory(func):
    """Decorator to profile the memory usage of a function using tracemalloc."""
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
def profile_block(profile_type='time'):
    """Context manager to profile a block of code (time or memory)."""
    if profile_type == 'time':
        _thread_local.start_time = time.perf_counter()  # Set the start time in thread-local storage
        try:
            yield
        finally:
            end_time = time.perf_counter()
            if hasattr(_thread_local, 'start_time'):
                time_taken = end_time - _thread_local.start_time
                logging.info(f"Code block took {time_taken:.4f} seconds")
            else:
                logging.warning("Thread-local start time not set for profiling block.")
    elif profile_type == 'memory':
        tracemalloc.start()
        try:
            yield
        finally:
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            logging.info(f"Code block used {peak / 1024:.2f} KB of memory (peak)")
    else:
        logging.error(f"Unknown profile_type: '{profile_type}', use 'time' or 'memory'")
        raise ValueError(f"Unknown profile_type: '{profile_type}', use 'time' or 'memory'")

@contextmanager
def profile_line(profile_type='time'):
    """Context manager to profile specific lines of code (time or memory)."""
    if profile_type == 'time':
        _thread_local.start_time = time.perf_counter()  # Set the start time in thread-local storage
        try:
            yield
        finally:
            end_time = time.perf_counter()
            if hasattr(_thread_local, 'start_time'):
                time_taken = end_time - _thread_local.start_time
                logging.info(f"Line(s) took {time_taken:.4f} seconds")
            else:
                logging.warning("Thread-local start time not set for profiling line.")
    elif profile_type == 'memory':
        tracemalloc.start()
        try:
            yield
        finally:
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            logging.info(f"Line(s) used {peak / 1024:.2f} KB of memory (peak)")
    else:
        logging.error(f"Unknown profile_type: '{profile_type}', use 'time' or 'memory'")
        raise ValueError(f"Unknown profile_type: '{profile_type}', use 'time' or 'memory'")
