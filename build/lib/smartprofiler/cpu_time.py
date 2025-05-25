import time
import logging
import threading
import functools
from contextlib import contextmanager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Thread-local storage to handle per-thread CPU time data
_thread_local = threading.local()

def profile_cpu_time(func):
    """Decorator to profile the CPU time used by a function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.process_time()  # Start CPU time tracking for the current thread
        try:
            result = func(*args, **kwargs)
        finally:
            end_time = time.process_time()  # End CPU time tracking
            logging.info(f"Function '{func.__name__}' used {end_time - start_time:.4f} seconds of CPU time")
        return result
    return wrapper

@contextmanager
def profile_block(profile_type='cpu_time'):
    """Context manager to profile a block of code (CPU time)."""
    if profile_type == 'cpu_time':
        _thread_local.start_time = time.process_time()  # Set the start time in thread-local storage
        try:
            yield
        finally:
            end_time = time.process_time()  # Capture end time
            if hasattr(_thread_local, 'start_time'):
                cpu_time_taken = end_time - _thread_local.start_time  # Calculate the CPU time used
                logging.info(f"Code block took {cpu_time_taken:.4f} seconds of CPU time")
            else:
                logging.warning("Thread-local start time not set for profiling block.")
    else:
        logging.error(f"Unknown profile_type: '{profile_type}', use 'cpu_time'")
        raise ValueError(f"Unknown profile_type: '{profile_type}', use 'cpu_time'")

@contextmanager
def profile_line(profile_type='cpu_time'):
    """Context manager to profile a specific line of code (CPU time)."""
    if profile_type == 'cpu_time':
        _thread_local.start_time = time.process_time()  # Set the start time for the current thread
        try:
            yield
        finally:
            end_time = time.process_time()  # Capture the end time
            if hasattr(_thread_local, 'start_time'):
                cpu_time_taken = end_time - _thread_local.start_time  # Calculate the CPU time used
                logging.info(f"Line(s) took {cpu_time_taken:.4f} seconds of CPU time")
            else:
                logging.warning("Thread-local start time not set for profiling line.")
    else:
        logging.error(f"Unknown profile_type: '{profile_type}', use 'cpu_time'")
        raise ValueError(f"Unknown profile_type: '{profile_type}', use 'cpu_time'")
