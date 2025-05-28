from typing import Any, Optional, Union
import logging
from abc import ABC, abstractmethod

class LoggerInterface(ABC):
    """Abstract base class defining the required logging interface."""
    
    @abstractmethod
    def info(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log an info message."""
        pass
    
    @abstractmethod
    def error(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log an error message."""
        pass
    
    @abstractmethod
    def debug(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log a debug message."""
        pass
    
    @abstractmethod
    def warning(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log a warning message."""
        pass
    
    @abstractmethod
    def log(self, level: int, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log a message at the specified level."""
        pass

class LoggerAdapter(LoggerInterface):
    """Adapter for different logging libraries to provide a consistent interface."""
    
    def __init__(self, logger: Any):
        """
        Initialize the adapter with a logger object.
        
        Args:
            logger: Any logger object that implements at least some of the standard logging methods.
                   Can be logging.Logger, loguru.Logger, structlog.BoundLogger, or any custom logger.
        """
        self._logger = logger
        self._validate_logger()
    
    def _validate_logger(self) -> None:
        """Validate that the logger has at least the basic required methods."""
        required_methods = ['info', 'error', 'debug', 'warning', 'log']
        missing_methods = [method for method in required_methods if not hasattr(self._logger, method)]
        
        if missing_methods:
            raise ValueError(
                f"Logger must implement at least these methods: {', '.join(required_methods)}. "
                f"Missing methods: {', '.join(missing_methods)}"
            )
    
    def _get_log_level_int(self, level: Union[str, int]) -> int:
        """Convert string log level to integer if needed."""
        if isinstance(level, str):
            level = level.upper()
            level_map = {
                'DEBUG': logging.DEBUG,
                'INFO': logging.INFO,
                'WARNING': logging.WARNING,
                'ERROR': logging.ERROR,
                'CRITICAL': logging.CRITICAL
            }
            if level not in level_map:
                raise ValueError(f"Invalid log level: {level}")
            return level_map[level]
        return level

    def info(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log an info message."""
        self._logger.info(msg, *args, **kwargs)
    
    def error(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log an error message."""
        self._logger.error(msg, *args, **kwargs)
    
    def debug(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log a debug message."""
        self._logger.debug(msg, *args, **kwargs)
    
    def warning(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log a warning message."""
        self._logger.warning(msg, *args, **kwargs)
    
    def log(self, level: Union[str, int], msg: str, *args: Any, **kwargs: Any) -> None:
        """Log a message at the specified level."""
        level_int = self._get_log_level_int(level)
        self._logger.log(level_int, msg, *args, **kwargs)
    
    def setLevel(self, level: int) -> None:
        """Set the logging level if the logger supports it."""
        if hasattr(self._logger, 'setLevel'):
            self._logger.setLevel(level)
    
    def addHandler(self, handler: Any) -> None:
        """Add a handler if the logger supports it."""
        if hasattr(self._logger, 'addHandler'):
            self._logger.addHandler(handler)
    
    @property
    def handlers(self) -> list:
        """Get the logger's handlers if available."""
        return getattr(self._logger, 'handlers', []) 