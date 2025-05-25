import psutil
import logging
from contextlib import contextmanager
from typing import Callable, Optional, Dict, Tuple
from .base_profiler import BaseProfiler

class DiskProfiler(BaseProfiler):
    """Profiler for measuring disk I/O and usage."""

    def __init__(
        self,
        disk_path: str = '/',
        logger: Optional[logging.Logger] = None,
        disk_metrics: Optional[Dict[str, bool]] = None,
         **kwargs
    ):
        super().__init__(logger, **kwargs)
        self.disk_path = disk_path
        self.disk_metrics = {
            'read_bytes': True,
            'write_bytes': True,
            'read_count': True,
            'write_count': True,
            'disk_usage': True,
        }
        if disk_metrics:
            self.disk_metrics.update(disk_metrics)

    def _get_disk_stats(self) -> Tuple[psutil._common.sdiskio, psutil._common.sdiskusage]:
        """Get current disk I/O and usage stats."""
        try:
            io_stats = psutil.disk_io_counters()
            usage_stats = psutil.disk_usage(self.disk_path)
            return io_stats, usage_stats
        except psutil.Error as e:
            self.logger.error(f"Error retrieving disk stats: {e}")
            raise

    def _log_disk_diff(
        self,
        label: str,
        before_io: psutil._common.sdiskio,
        after_io: psutil._common.sdiskio,
        before_usage: psutil._common.sdiskusage,
        after_usage: psutil._common.sdiskusage
    ):
        """Log and store the difference in disk I/O and usage stats."""
        metrics = {}
        if self.disk_metrics.get('read_bytes'):
            metrics['read_bytes'] = after_io.read_bytes - before_io.read_bytes
            self.logger.info(f"{label} - Bytes read: {metrics['read_bytes']}")
        if self.disk_metrics.get('write_bytes'):
            metrics['write_bytes'] = after_io.write_bytes - before_io.write_bytes
            self.logger.info(f"{label} - Bytes written: {metrics['write_bytes']}")
        if self.disk_metrics.get('read_count'):
            metrics['read_count'] = after_io.read_count - before_io.read_count
            self.logger.info(f"{label} - Read operations: {metrics['read_count']}")
        if self.disk_metrics.get('write_count'):
            metrics['write_count'] = after_io.write_count - before_io.write_count
            self.logger.info(f"{label} - Write operations: {metrics['write_count']}")
        if self.disk_metrics.get('disk_usage'):
            metrics['disk_usage'] = {
                'before': {
                    'total': before_usage.total / (1024 ** 3),
                    'used': before_usage.used / (1024 ** 3),
                    'free': before_usage.free / (1024 ** 3)
                },
                'after': {
                    'total': after_usage.total / (1024 ** 3),
                    'used': after_usage.used / (1024 ** 3),
                    'free': after_usage.free / (1024 ** 3)
                }
            }
            self.logger.info(
                f"{label} - Disk space before: Total={metrics['disk_usage']['before']['total']:.2f}GB, "
                f"Used={metrics['disk_usage']['before']['used']:.2f}GB, Free={metrics['disk_usage']['before']['free']:.2f}GB"
            )
            self.logger.info(
                f"{label} - Disk space after: Total={metrics['disk_usage']['after']['total']:.2f}GB, "
                f"Used={metrics['disk_usage']['after']['used']:.2f}GB, Free={metrics['disk_usage']['after']['free']:.2f}GB"
            )
        self.stats.append({'label': label, 'metrics': metrics})

    def profile_function(self, func: Callable) -> Callable:
        """Decorator to profile disk I/O and usage of a function."""
        def profile_logic(func, *args, **kwargs):
            before_io, before_usage = self._get_disk_stats()
            try:
                result = func(*args, **kwargs)
            finally:
                after_io, after_usage = self._get_disk_stats()
                self._log_disk_diff(f"Function '{func.__name__}'", before_io, after_io, before_usage, after_usage)
            return result
        return self._wrap_function(func, profile_logic)

    @contextmanager
    def profile_block(self, label: str = "Disk block"):
        """Context manager to profile disk I/O and usage for a block of code."""
        before_io, before_usage = self._get_disk_stats()
        try:
            yield
        finally:
            after_io, after_usage = self._get_disk_stats()
            self._log_disk_diff(label, before_io, after_io, before_usage, after_usage)

    @contextmanager
    def profile_line(self, label: str = "Disk line(s)"):
        """Context manager to profile disk I/O and usage for a specific line or small block."""
        before_io, before_usage = self._get_disk_stats()
        try:
            yield
        finally:
            after_io, after_usage = self._get_disk_stats()
            self._log_disk_diff(label, before_io, after_io, before_usage, after_usage)
