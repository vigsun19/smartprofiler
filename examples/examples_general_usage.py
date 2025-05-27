import time
import requests
import logging
import argparse
from smartprofiler import CPUProfiler, DiskProfiler, FunctionProfiler, MemoryProfiler, NetworkProfiler

def setup_logger(logger_type: str = None) -> logging.Logger:
    """
    Set up and return a logger based on the specified type.
    
    Args:
        logger_type: Type of logger to use ('loguru', 'structlog', or None for default)
    
    Returns:
        Configured logger instance
    """
    if logger_type == 'loguru':
        try:
            from loguru import logger
            return logger
        except ImportError:
            print("Loguru is not installed. Falling back to default logger.")
            print("Install it with: pip install loguru")
            return setup_default_logger()
    
    elif logger_type == 'structlog':
        try:
            import structlog
            return structlog.get_logger()
        except ImportError:
            print("Structlog is not installed. Falling back to default logger.")
            print("Install it with: pip install structlog")
            return setup_default_logger()
    
    return setup_default_logger()

def setup_default_logger() -> logging.Logger:
    """Set up and return the default Python logger."""
    logger = logging.getLogger('smartprofiler_examples')
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    return logger

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='SmartProfiler Examples with Different Loggers')
    parser.add_argument('--logger', choices=['loguru', 'structlog'], 
                      help='Logger type to use (default: standard Python logger)')
    args = parser.parse_args()

    # Set up the selected logger
    logger = setup_logger(args.logger)
    print(f"\nUsing {args.logger if args.logger else 'default'} logger\n")

    # Initialize profilers with custom logging settings
    cpu_profiler = CPUProfiler(time_func='execution_time', logger=logger, log_level=logging.DEBUG)
    disk_profiler = DiskProfiler(disk_path='/tmp', disk_metrics={'write_bytes': True, 'disk_usage': False}, logger=logger, log_level=logging.DEBUG)
    func_profiler = FunctionProfiler(logger=logger, log_level=logging.DEBUG)
    mem_profiler = MemoryProfiler(logger=logger, log_level=logging.DEBUG)
    net_profiler = NetworkProfiler(network_metrics={'bytes_sent': True, 'bytes_recv': True}, logger=logger, log_level=logging.DEBUG)

    # Example 1: Profile a CPU-intensive function
    @cpu_profiler.profile_function
    def compute_fibonacci(n):
        if n <= 1:
            return n
        return compute_fibonacci(n-1) + compute_fibonacci(n-2)

    print("Profiling a CPU-intensive function (Fibonacci calculation):")
    compute_fibonacci(20)
    cpu_profiler.summarize_stats()
    print()

    # Example 2: Profile a disk-intensive block
    print("Profiling a disk-intensive block (writing to a file):")
    with disk_profiler.profile_block("disk_write_block"):
        with open('/tmp/test_file.txt', 'w') as f:
            f.write("Sample data " * 1000)
    disk_profiler.summarize_stats()
    print()

    # Example 3: Profile function calls in a block
    print("Profiling function calls in a block (nested calls):")
    with func_profiler.profile_block("nested_calls"):
        def inner_func():
            pass
        for _ in range(100):
            inner_func()
    func_profiler.summarize_stats()
    print()

    # Example 4: Profile memory usage for a single line
    print("Profiling memory usage for a single line (large list allocation):")
    with mem_profiler.profile_line("large_list_allocation"):
        large_list = [i for i in range(10**6)]
    mem_profiler.summarize_stats()
    print()

    # Example 5: Profile network I/O with logging disabled
    print("Profiling network I/O with logging disabled (API request):")
    net_profiler_silent = NetworkProfiler(network_metrics={'bytes_sent': True, 'bytes_recv': True}, logger=logger, enable_logging=False)
    with net_profiler_silent.profile_block("api_request"):
        requests.get('https://api.github.com')
    net_profiler_silent.summarize_stats()  # No log messages will be written
    # Manually print stats to show they were collected
    stats = net_profiler_silent.get_stats()
    print("Network stats (manually printed):", stats)

if __name__ == "__main__":
    main()
