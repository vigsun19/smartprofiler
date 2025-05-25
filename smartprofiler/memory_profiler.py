import tracemalloc
import logging
from contextlib import contextmanager
from typing import Callable, Optional
from .base_profiler import BaseProfiler

class MemoryProfiler(BaseProfiler):
    """Profiler for measuring memory usage."""

    def __init__(self, logger: Optional[logging.Logger] = None,  **kwargs):
        super().__init__(logger,  **kwargs)

    def profile_function(self, func: Callable) -> Callable:
        """Decorator to profile memory usage of a function."""
        def profile_logic(func, *args, **kwargs):
            tracemalloc.start()
            try:
                result = func(*args, **kwargs)
            finally:
                current, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                metrics = {'current_mb': current / (1024 ** 2), 'peak_mb': peak / (1024 ** 2)}
                self.stats.append({'label': f"Function '{func.__name__}'", 'metrics': metrics})
                self.logger.info(
                    f"Function '{func.__name__}' memory usage: Current={metrics['current_mb']:.2f}MB, "
                    f"Peak={metrics['peak_mb']:.2f}MB"
                )
            return result
        return self._wrap_function(func, profile_logic)

    @contextmanager
    def profile_block(self, label: str = "Memory block"):
        """Context manager to profile memory usage for a block of code."""
        tracemalloc.start()
        try:
            yield
        finally:
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            metrics = {'current_mb': current / (1024 ** 2), 'peak_mb': peak / (1024 ** 2)}
            self.stats.append({'label': label, 'metrics': metrics})
            self.logger.info(
                f"{label} memory usage: Current={metrics['current_mb']:.2f}MB, Peak={metrics['peak_mb']:.2f}MB"
            )

    @contextmanager
    def profile_line(self, label: str = "Memory line(s)"):
        """Context manager to profile memory usage for a specific line or small block."""
        tracemalloc.start()
        try:
            yield
        finally:
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            metrics = {'current_mb': current / (1024 ** 2), 'peak_mb': peak / (1024 ** 2)}
            self.stats.append({'label': label, 'metrics': metrics})
            self.logger.info(
                f"{label} memory usage: Current={metrics['current_mb']:.2f}MB, Peak={metrics['peak_mb']:.2f}MB"
            )
            