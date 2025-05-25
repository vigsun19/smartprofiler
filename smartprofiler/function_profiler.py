import sys
import logging
from contextlib import contextmanager
from typing import Callable, Optional
from .base_profiler import BaseProfiler, _thread_local

class FunctionProfiler(BaseProfiler):
    """Profiler for counting function calls."""

    def __init__(self, logger: Optional[logging.Logger] = None,  **kwargs):
        super().__init__(logger, **kwargs)
        self.call_count = 0

    def _trace_function(self, frame, event, arg):
        """Trace function to count function calls."""
        if event == 'call':
            self.call_count += 1
        return self._trace_function

    def profile_function(self, func: Callable) -> Callable:
        """Decorator to profile function call counts."""
        def profile_logic(func, *args, **kwargs):
            self.call_count = 0
            sys.settrace(self._trace_function)
            try:
                result = func(*args, **kwargs)
            finally:
                sys.settrace(None)
                metrics = {'call_count': self.call_count}
                self.stats.append({'label': f"Function '{func.__name__}'", 'metrics': metrics})
                self.logger.info(f"Function '{func.__name__}' made {self.call_count} function calls")
            return result
        return self._wrap_function(func, profile_logic)

    @contextmanager
    def profile_block(self, label: str = "Function call block"):
        """Context manager to profile function calls in a block of code."""
        self.call_count = 0
        sys.settrace(self._trace_function)
        try:
            yield
        finally:
            sys.settrace(None)
            metrics = {'call_count': self.call_count}
            self.stats.append({'label': label, 'metrics': metrics})
            self.logger.info(f"{label} made {self.call_count} function calls")

    @contextmanager
    def profile_line(self, label: str = "Function call line(s)"):
        """Context manager to profile function calls for a specific line or small block."""
        self.call_count = 0
        sys.settrace(self._trace_function)
        try:
            yield
        finally:
            sys.settrace(None)
            metrics = {'call_count': self.call_count}
            self.stats.append({'label': label, 'metrics': metrics})
            self.logger.info(f"{label} made {self.call_count} function calls")
