import psutil
import logging
from contextlib import contextmanager
from typing import Callable, Optional, Dict
from .base_profiler import BaseProfiler

class NetworkProfiler(BaseProfiler):
    """Profiler for measuring network I/O."""

    def __init__(
        self,
        logger: Optional[logging.Logger] = None,
        network_metrics: Optional[Dict[str, bool]] = None,
        **kwargs
    ):
        """
        Initialize the NetworkProfiler.

        Args:
            logger: Custom logger instance (default: None, uses default logger).
            network_metrics: Dict to enable/disable network metrics (e.g., {'bytes_sent': True}).
            **kwargs: Additional arguments passed to BaseProfiler (e.g., log_level, enable_logging).
        """
        super().__init__(logger=logger, **kwargs)
        self.network_metrics = {
            'bytes_sent': True,
            'bytes_recv': True,
            'packets_sent': True,
            'packets_recv': True,
        }
        if network_metrics:
            self.network_metrics.update(network_metrics)

    def _get_network_stats(self) -> psutil._common.snetio:
        """Get current network I/O stats."""
        try:
            return psutil.net_io_counters()
        except psutil.Error as e:
            if self.enable_logging:
                self.logger.error(f"Error retrieving network stats: {e}")
            raise

    def _log_network_diff(self, label: str, before: psutil._common.snetio, after: psutil._common.snetio):
        """Log and store the difference in network I/O stats."""
        metrics = {}
        if self.network_metrics.get('bytes_sent'):
            metrics['bytes_sent'] = after.bytes_sent - before.bytes_sent
            if self.enable_logging:
                self.logger.log(self.log_level, f"{label} - Bytes sent: {metrics['bytes_sent']}")
        if self.network_metrics.get('bytes_recv'):
            metrics['bytes_recv'] = after.bytes_recv - before.bytes_recv
            if self.enable_logging:
                self.logger.log(self.log_level, f"{label} - Bytes received: {metrics['bytes_recv']}")
        if self.network_metrics.get('packets_sent'):
            metrics['packets_sent'] = after.packets_sent - before.packets_sent
            if self.enable_logging:
                self.logger.log(self.log_level, f"{label} - Packets sent: {metrics['packets_sent']}")
        if self.network_metrics.get('packets_recv'):
            metrics['packets_recv'] = after.packets_recv - before.packets_recv
            if self.enable_logging:
                self.logger.log(self.log_level, f"{label} - Packets received: {metrics['packets_recv']}")
        self.stats.append({'label': label, 'metrics': metrics})

    def profile_function(self, func: Callable) -> Callable:
        """Decorator to profile network I/O of a function."""
        def profile_logic(func, *args, **kwargs):
            before = self._get_network_stats()
            try:
                result = func(*args, **kwargs)
            finally:
                after = self._get_network_stats()
                self._log_network_diff(f"Function '{func.__name__}'", before, after)
            return result
        return self._wrap_function(func, profile_logic)

    @contextmanager
    def profile_block(self, label: str = "Network block"):
        """Context manager to profile network I/O for a block of code."""
        before = self._get_network_stats()
        try:
            yield
        finally:
            after = self._get_network_stats()
            self._log_network_diff(label, before, after)

    @contextmanager
    def profile_line(self, label: str = "Network line(s)"):
        """Context manager to profile network I/O for a specific line or small block."""
        before = self._get_network_stats()
        try:
            yield
        finally:
            after = self._get_network_stats()
            self._log_network_diff(label, before, after)
