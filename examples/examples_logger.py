"""
Examples demonstrating the usage of the LoggerAdapter with different logging backends.
This example shows how to use the LoggerAdapter with standard logging, loguru, and structlog.
"""

import logging
from smartprofiler.logger_adapter import LoggerAdapter

# Example 1: Using standard logging
def example_standard_logging():
    print("\n=== Example 1: Standard Logging ===")
    
    # Setup standard logger
    logger = logging.getLogger('standard_logger')
    logger.setLevel(logging.INFO)
    
    # Add console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
    logger.addHandler(console_handler)
    
    # Create adapter
    adapter = LoggerAdapter(logger)
    
    # Demonstrate different log levels
    adapter.debug("This debug message won't show (level is INFO)")
    adapter.info("This is an info message")
    adapter.warning("This is a warning message")
    adapter.error("This is an error message")
    
    # Demonstrate custom log level
    adapter.log(logging.CRITICAL, "This is a critical message")

# Example 2: Using loguru (if available)
def example_loguru():
    try:
        from loguru import logger as loguru_logger
        print("\n=== Example 2: Loguru ===")
        
        # Create adapter with loguru logger
        adapter = LoggerAdapter(loguru_logger)
        
        # Demonstrate different log levels
        adapter.debug("This is a debug message")
        adapter.info("This is an info message")
        adapter.warning("This is a warning message")
        adapter.error("This is an error message")
        
    except ImportError:
        print("\n=== Example 2: Loguru ===")
        print("Loguru is not installed. Install it with: pip install loguru")

# Example 3: Using structlog (if available)
def example_structlog():
    try:
        import structlog
        print("\n=== Example 3: Structlog ===")
        
        # Configure structlog
        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.JSONRenderer()
            ]
        )
        
        # Create structlog logger
        logger = structlog.get_logger()
        
        # Create adapter
        adapter = LoggerAdapter(logger)
        
        # Demonstrate different log levels
        adapter.debug("This is a debug message")
        adapter.info("This is an info message")
        adapter.warning("This is a warning message")
        adapter.error("This is an error message")
        
    except ImportError:
        print("\n=== Example 3: Structlog ===")
        print("Structlog is not installed. Install it with: pip install structlog")

def main():
    print("Logger Adapter Examples")
    print("======================")
    
    # Run all examples
    example_standard_logging()
    example_loguru()
    example_structlog()

if __name__ == "__main__":
    main() 