import psutil
import logging
from contextlib import contextmanager
from functools import wraps

# Configure logging for disk profiling
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def profile_method(func):
    """Decorator to profile disk usage of a method/function."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        disk_before = psutil.disk_io_counters()
        disk_usage_before = psutil.disk_usage('/')
        result = func(*args, **kwargs)
        disk_after = psutil.disk_io_counters()
        disk_usage_after = psutil.disk_usage('/')

        logging.info(f"Function '{func.__name__}' disk read bytes: {disk_after.read_bytes - disk_before.read_bytes}, "
                     f"write bytes: {disk_after.write_bytes - disk_before.write_bytes}")
        logging.info(f"Disk space before: Total={disk_usage_before.total / (1024 ** 3):.2f}GB, "
                     f"Used={disk_usage_before.used / (1024 ** 3):.2f}GB, Free={disk_usage_before.free / (1024 ** 3):.2f}GB")
        logging.info(f"Disk space after: Total={disk_usage_after.total / (1024 ** 3):.2f}GB, "
                     f"Used={disk_usage_after.used / (1024 ** 3):.2f}GB, Free={disk_usage_after.free / (1024 ** 3):.2f}GB")
        return result

    return wrapper


@contextmanager
def profile_block():
    """Context manager to profile disk I/O usage."""
    disk_before = psutil.disk_io_counters()
    disk_usage_before = psutil.disk_usage('/')
    try:
        yield
    finally:
        disk_after = psutil.disk_io_counters()
        disk_usage_after = psutil.disk_usage('/')

        # Log disk I/O stats
        logging.info(f"Disk I/O before: {disk_before}")
        logging.info(f"Disk I/O after: {disk_after}")
        logging.info(f"Bytes read: {disk_after.read_bytes - disk_before.read_bytes}")
        logging.info(f"Bytes written: {disk_after.write_bytes - disk_before.write_bytes}")
        logging.info(f"Read operations: {disk_after.read_count - disk_before.read_count}")
        logging.info(f"Write operations: {disk_after.write_count - disk_before.write_count}")

        # Log disk space stats
        logging.info(f"Disk space before: Total={disk_usage_before.total / (1024 ** 3):.2f}GB, "
                     f"Used={disk_usage_before.used / (1024 ** 3):.2f}GB, Free={disk_usage_before.free / (1024 ** 3):.2f}GB")
        logging.info(f"Disk space after: Total={disk_usage_after.total / (1024 ** 3):.2f}GB, "
                     f"Used={disk_usage_after.used / (1024 ** 3):.2f}GB, Free={disk_usage_after.free / (1024 ** 3):.2f}GB")