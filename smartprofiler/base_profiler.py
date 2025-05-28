import logging
import threading
from abc import ABC, abstractmethod
from typing import Optional, Callable, Dict, List, Any
from functools import wraps
from .logger_adapter import LoggerAdapter

# Thread-local storage for thread-safe profiling
_thread_local = threading.local()

class BaseProfiler(ABC):
    """Abstract base class for profiling implementations with aggregate statistics."""

    def __init__(self, logger: Optional[Any] = None, log_level: int = logging.INFO, enable_logging: bool = True):
        """
        Initialize the profiler with an optional custom logger, log level, and logging enablement.

        Args:
            logger: Custom logger instance (default: None, uses default logger).
                  Can be logging.Logger, loguru.Logger, structlog.BoundLogger, or any custom logger.
            log_level: Logging level to use (e.g., logging.INFO, logging.DEBUG).
            enable_logging: If False, disables logging of metrics.
        """
        # Create a default logger if none provided
        default_logger = logging.getLogger(__name__)
        if not default_logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            default_logger.addHandler(handler)
        
        # Wrap the logger with our adapter
        self.logger = LoggerAdapter(logger or default_logger)
        self.logger.setLevel(log_level)
        self.log_level = log_level
        self.enable_logging = enable_logging
        # Store profiling results for aggregate statistics
        self.stats: List[Dict] = []

    @abstractmethod
    def profile_function(self, func: Callable) -> Callable:
        """Decorator to profile a function."""
        pass

    @abstractmethod
    def profile_block(self, label: str):
        """Context manager to profile a code block."""
        pass

    @abstractmethod
    def profile_line(self, label: str):
        """Context manager to profile a specific line or small block."""
        pass

    def _wrap_function(self, func: Callable, profile_logic: Callable) -> Callable:
        """Helper to wrap a function with profiling logic."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            return profile_logic(func, *args, **kwargs)
        return wrapper

    def get_stats(self) -> List[Dict]:
        """Return collected profiling statistics."""
        return self.stats

    def clear_stats(self):
        """Clear collected profiling statistics."""
        self.stats.clear()

    def summarize_stats(self):
        """Log a summary of collected statistics."""
        if not self.enable_logging:
            return
        if not self.stats:
            self.logger.log(self.log_level, "No profiling statistics available.")
            return
        self.logger.log(self.log_level, f"Summary of {len(self.stats)} profiling events:")
        for stat in self.stats:
            self.logger.log(self.log_level, f"{stat['label']}: {stat['metrics']}")
