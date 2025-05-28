"""
Examples demonstrating the usage of different logging backends with the SmartProfiler.
This example shows how to use standard logging, loguru, and structlog with CPU profiling.
"""

import logging
import time
from smartprofiler import CPUProfiler
from smartprofiler.logger_adapter import LoggerAdapter

def compute_fibonacci(n: int) -> int:
    """Compute the nth Fibonacci number."""
    if n <= 1:
        return n
    return compute_fibonacci(n - 1) + compute_fibonacci(n - 2)

# Example 1: Using standard logging
def example_standard_logging():
    print("\n=== Example 1: Standard Logging with CPU Profiling ===")
    
    # Setup standard logger
    logger = logging.getLogger('standard_logger')
    logger.setLevel(logging.INFO)
    
    # Add console handler with detailed formatting
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(console_handler)
    
    # Create CPU profiler with standard logger
    cpu_profiler = CPUProfiler(
        time_func='execution_time',
        logger=logger,
        log_level=logging.INFO
    )
    
    # Profile a CPU-intensive function
    @cpu_profiler.profile_function
    def profiled_fibonacci(n: int) -> int:
        return compute_fibonacci(n)
    
    print("Profiling Fibonacci calculation with standard logging:")
    result = profiled_fibonacci(20)
    print(f"Fibonacci(20) = {result}")
    cpu_profiler.summarize_stats()

# Example 2: Using loguru (if available)
def example_loguru():
    try:
        from loguru import logger as loguru_logger
        print("\n=== Example 2: Loguru with CPU Profiling ===")
        
        # Create CPU profiler with default loguru logger
        cpu_profiler = CPUProfiler(
            time_func='execution_time',
            logger=loguru_logger,
            log_level="INFO"
        )
        
        # Profile a CPU-intensive function
        @cpu_profiler.profile_function
        def profiled_fibonacci(n: int) -> int:
            return compute_fibonacci(n)
        
        print("Profiling Fibonacci calculation with loguru:")
        result = profiled_fibonacci(20)
        print(f"Fibonacci(20) = {result}")
        cpu_profiler.summarize_stats()
        
    except ImportError:
        print("\n=== Example 2: Loguru ===")
        print("Loguru is not installed. Install it with: pip install loguru")

# Example 3: Using structlog (if available)
def example_structlog():
    try:
        import structlog
        print("\n=== Example 3: Structlog with CPU Profiling ===")
        
        # Create structlog logger with default configuration
        logger = structlog.get_logger()
        
        # Create CPU profiler with structlog logger
        cpu_profiler = CPUProfiler(
            time_func='execution_time',
            logger=logger,
            log_level="INFO"
        )
        
        # Profile a CPU-intensive function
        @cpu_profiler.profile_function
        def profiled_fibonacci(n: int) -> int:
            return compute_fibonacci(n)
        
        print("Profiling Fibonacci calculation with structlog:")
        result = profiled_fibonacci(20)
        print(f"Fibonacci(20) = {result}")
        cpu_profiler.summarize_stats()
        
    except ImportError:
        print("\n=== Example 3: Structlog ===")
        print("Structlog is not installed. Install it with: pip install structlog")

def main():
    print("SmartProfiler Logger Examples")
    print("============================")
    
    # Run all examples
    example_standard_logging()
    example_loguru()
    example_structlog()

if __name__ == "__main__":
    main() 