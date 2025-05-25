import psutil
import logging
from contextlib import contextmanager
from functools import wraps

# Configure logging for network profiling
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def profile_method(func):
    """Decorator to profile network usage of a method/function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        net_before = psutil.net_io_counters()
        result = func(*args, **kwargs)
        net_after = psutil.net_io_counters()
        logging.info(f"Function '{func.__name__}' sent {net_after.bytes_sent - net_before.bytes_sent} bytes, "
                     f"received {net_after.bytes_recv - net_before.bytes_recv} bytes")
        return result
    return wrapper

@contextmanager
def profile_block():
    """Context manager to profile network usage."""
    net_before = psutil.net_io_counters()
    try:
        yield
    finally:
        net_after = psutil.net_io_counters()
        logging.info(f"Network usage before: {net_before}")
        logging.info(f"Network usage after: {net_after}")
        logging.info(f"Bytes sent: {net_after.bytes_sent - net_before.bytes_sent}")
        logging.info(f"Bytes received: {net_after.bytes_recv - net_before.bytes_recv}")
        logging.info(f"Packets sent: {net_after.packets_sent - net_before.packets_sent}")
        logging.info(f"Packets received: {net_after.packets_recv - net_before.packets_recv}")