import time
import random
import requests
import logging
from smartprofiler import CPUProfiler, DiskProfiler, FunctionProfiler, MemoryProfiler, NetworkProfiler, plot_profiling_stats

def main():
    # Set up a logger for minimal output
    logger = logging.getLogger('smartprofiler_visualization')
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)

    # Example 1: CPU, Disk, and Memory Profiling
    print("Generating visualization for CPU, Disk, and Memory profiling...")
    cpu_profiler = CPUProfiler(time_func='execution_time', logger=logger)
    disk_profiler = DiskProfiler(disk_path='/tmp', disk_metrics={'write_bytes': True, 'disk_usage': False}, logger=logger)
    mem_profiler = MemoryProfiler(logger=logger)

    # CPU-intensive task (matrix multiplication)
    @cpu_profiler.profile_function
    @mem_profiler.profile_function
    def matrix_multiply():
        size = 500
        matrix_a = [[random.random() for _ in range(size)] for _ in range(size)]
        matrix_b = [[random.random() for _ in range(size)] for _ in range(size)]
        result = [[0 for _ in range(size)] for _ in range(size)]
        for i in range(size):
            for j in range(size):
                for k in range(size):
                    result[i][j] += matrix_a[i][k] * matrix_b[k][j]
        return result

    # Disk-intensive task (writing large files)
    @disk_profiler.profile_function
    @mem_profiler.profile_function
    def write_large_file():
        with open('/tmp/large_file.txt', 'w') as f:
            for _ in range(1000):
                f.write("Sample data " * 1000 + "\n")

    # Memory-intensive task (large list allocation)
    @cpu_profiler.profile_function
    @mem_profiler.profile_function
    def allocate_large_list():
        large_list = [random.random() for _ in range(10**7)]
        return sum(large_list)

    # Mixed workload (block profiling)
    with cpu_profiler.profile_block("mixed_workload"):
        with disk_profiler.profile_block("mixed_workload"):
            with mem_profiler.profile_block("mixed_workload"):
                data = [random.random() for _ in range(5**6)]
                time.sleep(0.5)
                with open('/tmp/mixed_file.txt', 'w') as f:
                    f.write(str(data))

    # Line profiling (quick computation)
    with cpu_profiler.profile_line("quick_computation"):
        with mem_profiler.profile_line("quick_computation"):
            sum([i**2 for i in range(1000)])

    # Run the examples
    matrix_multiply()
    write_large_file()
    allocate_large_list()

    # Generate visualization for CPU, Disk, Memory
    plot_profiling_stats(
        [cpu_profiler, disk_profiler, mem_profiler],
        output_dir='images',
        output_file='profiling_stats_cpu_disk_memory.png'
    )

    # Example 2: Network and Function Call Profiling
    print("Generating visualization for Network and Function Call profiling...")
    func_profiler = FunctionProfiler(logger=logger)
    net_profiler = NetworkProfiler(network_metrics={'bytes_sent': True, 'bytes_recv': True}, logger=logger)

    # Network-intensive task (multiple API requests)
    @net_profiler.profile_function
    def fetch_multiple_apis():
        urls = [
            'https://api.github.com',
            'https://jsonplaceholder.typicode.com/posts',
            'https://httpbin.org/get'
        ]
        for url in urls:
            response = requests.get(url, stream=True)
            response.raw.read(1024 * 5)  # Read some data

    # Recursive function calls
    @func_profiler.profile_function
    def recursive_fibonacci(n):
        if n <= 1:
            return n
        return recursive_fibonacci(n-1) + recursive_fibonacci(n-2)

    # Network-intensive block (downloading data)
    with net_profiler.profile_block("download_data"):
        response = requests.get('https://api.github.com/users', stream=True)
        response.raw.read(1024 * 10)  # Read more data

    # Function call block (nested calls)
    with func_profiler.profile_block("nested_calls"):
        def inner_func():
            pass
        for _ in range(100):
            inner_func()

    # Line profiling (single network request)
    with net_profiler.profile_line("single_request"):
        requests.get('https://httpbin.org/get')

    # Line profiling (single function call)
    with func_profiler.profile_line("single_call"):
        def simple_func():
            pass
        simple_func()

    # Run the examples
    fetch_multiple_apis()
    recursive_fibonacci(10)  # Generates multiple function calls

    # Generate visualization for Network and Function Calls
    plot_profiling_stats(
        [func_profiler, net_profiler],
        output_dir='images',
        output_file='profiling_stats_network_function.png'
    )

if __name__ == "__main__":
    main()
