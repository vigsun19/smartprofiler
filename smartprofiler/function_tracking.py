import functools
import logging
import threading

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

_lock = threading.Lock()


def profile_call_count(func):
    """Decorator to track the number of times a function is called, thread-safe."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with _lock:
            wrapper.call_count += 1
            logging.info(f"Function '{func.__name__}' has been called {wrapper.call_count} times")
        return func(*args, **kwargs)

    wrapper.call_count = 0
    return wrapper
