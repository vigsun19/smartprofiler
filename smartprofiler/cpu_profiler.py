import time
import logging
from contextlib import contextmanager
from typing import Callable, Optional
from .base_profiler import BaseProfiler, _thread_local

# Supported time functions
TIME_FUNCTIONS = {
    'execution_time': (time.perf_counter, "high-resolution execution time"),
    'cpu_time': (time.process_time, "measures CPU time (excludes I/O wait)"),
    'wall_time': (time.time, "measures wall-clock time"),
}

class CPUProfiler(BaseProfiler):
    """Profiler for measuring execution time (CPU or wall-clock)."""

    def __init__(self, time_func: str = 'execution_time', logger: Optional[logging.Logger] = None, **kwargs):
        super().__init__(logger=logger, **kwargs)
        if time_func not in TIME_FUNCTIONS:
            raise ValueError(f"Unknown time_func: '{time_func}'. Supported: {list(TIME_FUNCTIONS.keys())}")
        self.time_func = TIME_FUNCTIONS[time_func][0]
        self.time_func_name = time_func

    def profile_function(self, func: Callable) -> Callable:
        """Decorator to profile the execution time of a function."""
        def profile_logic(func, *args, **kwargs):
            start_time = self.time_func()
            try:
                result = func(*args, **kwargs)
            finally:
                end_time = self.time_func()
                duration = end_time - start_time
                metrics = {self.time_func_name: duration}
                self.stats.append({'label': f"Function '{func.__name__}'", 'metrics': metrics})
                if self.enable_logging:
                    self.logger.log(self.log_level, f"Function '{func.__name__}' took {duration:.4f} seconds of {self.time_func_name}")
            return result
        return self._wrap_function(func, profile_logic)

    @contextmanager
    def profile_block(self, label: str = "Code block"):
        """Context manager to profile a block of code for time."""
        start_time = self.time_func()
        try:
            yield
        finally:
            end_time = self.time_func()
            duration = end_time - start_time
            metrics = {self.time_func_name: duration}
            self.stats.append({'label': label, 'metrics': metrics})
            if self.enable_logging:
                self.logger.log(self.log_level, f"{label} took {duration:.4f} seconds of {self.time_func_name}")

    @contextmanager
    def profile_line(self, label: str = "Line(s)"):
        """Context manager to profile a specific line or small block for time."""
        start_time = self.time_func()
        try:
            yield
        finally:
            end_time = self.time_func()
            duration = end_time - start_time
            metrics = {self.time_func_name: duration}
            self.stats.append({'label': label, 'metrics': metrics})
            if self.enable_logging:
                self.logger.log(self.log_level, f"{label} took {duration:.4f} seconds of {self.time_func_name}")
