import unittest
import logging
from io import StringIO
from smartprofiler.logger_adapter import LoggerAdapter

try:
    from loguru import logger as loguru_logger
    LOGURU_AVAILABLE = True
except ImportError:
    LOGURU_AVAILABLE = False

try:
    import structlog
    STRUCTLOG_AVAILABLE = True
except ImportError:
    STRUCTLOG_AVAILABLE = False

class TestLoggerAdapter(unittest.TestCase):
    def setUp(self):
        self.output = StringIO()
        self.handler = logging.StreamHandler(self.output)
        self.handler.setFormatter(logging.Formatter('%(message)s'))
        
        # Standard logging setup
        self.std_logger = logging.getLogger('test')
        self.std_logger.setLevel(logging.INFO)
        self.std_logger.addHandler(self.handler)
        
        # Loguru setup if available
        if LOGURU_AVAILABLE:
            loguru_logger.remove()  # Remove default handler
            loguru_logger.add(self.output, format="{message}")
        
        # Structlog setup if available
        if STRUCTLOG_AVAILABLE:
            structlog.configure(
                processors=[
                    structlog.processors.TimeStamper(fmt="iso"),
                    structlog.processors.JSONRenderer()
                ],
                logger_factory=structlog.PrintLoggerFactory(file=self.output)
            )
            self.struct_logger = structlog.get_logger()

    def test_standard_logger(self):
        """Test adapter with standard logging.Logger."""
        adapter = LoggerAdapter(self.std_logger)
        adapter.info("Test message")
        self.assertIn("Test message", self.output.getvalue())

    @unittest.skipIf(not LOGURU_AVAILABLE, "loguru not installed")
    def test_loguru_logger(self):
        """Test adapter with loguru.Logger."""
        adapter = LoggerAdapter(loguru_logger)
        adapter.info("Test message")
        self.assertIn("Test message", self.output.getvalue())

    @unittest.skipIf(not STRUCTLOG_AVAILABLE, "structlog not installed")
    def test_structlog_logger(self):
        """Test adapter with structlog.BoundLogger."""
        adapter = LoggerAdapter(self.struct_logger)
        adapter.info("Test message")
        output = self.output.getvalue()
        self.assertIn('"event": "Test message"', output)  # Check for message in JSON format
        self.assertIn('"timestamp"', output)  # Verify JSON format

    def test_invalid_logger(self):
        """Test adapter with an invalid logger object."""
        class InvalidLogger:
            pass
        
        with self.assertRaises(ValueError):
            LoggerAdapter(InvalidLogger())

    def test_log_levels(self):
        """Test all logging levels with standard logger."""
        adapter = LoggerAdapter(self.std_logger)
        
        # Test each level
        adapter.debug("Debug message")
        adapter.info("Info message")
        adapter.warning("Warning message")
        adapter.error("Error message")
        
        output = self.output.getvalue()
        self.assertNotIn("Debug message", output)  # Debug should not appear (level is INFO)
        self.assertIn("Info message", output)
        self.assertIn("Warning message", output)
        self.assertIn("Error message", output)

    def test_log_with_level(self):
        """Test log method with explicit level."""
        adapter = LoggerAdapter(self.std_logger)
        adapter.log(logging.WARNING, "Custom level message")
        self.assertIn("Custom level message", self.output.getvalue())

if __name__ == '__main__':
    unittest.main() 