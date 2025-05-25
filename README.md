# SmartProfiler

**SmartProfiler** is a comprehensive Python library designed to help you profile and optimize your code by tracking **execution time, disk I/O, memory usage, network I/O, and function call counts**. It provides an all-in-one solution for performance analysis, complete with integrated visualization to make sense of your profiling data. Whether you're debugging bottlenecks, optimizing resource usage, or monitoring function calls, SmartProfiler offers a simple and efficient toolset for your needs.

## Why SmartProfiler?

- **Multi-Faceted Profiling**: Profile execution time, disk I/O, memory usage, network I/O, and function calls in a single library, reducing the need for multiple tools.
- **Integrated Visualization**: Generate normalized bar charts with a single command to visualize performance metrics across different sections of your code.
- **Flexible Profiling**: Use decorators or context managers to profile at the function, block, or line level with minimal setup.
- **Lightweight**: Designed to introduce minimal performance overhead while providing accurate profiling data.
- **Detailed Logging**: Integration with Python's logging framework for real-time insights into your code's performance.

## Features

- **Function-Level Profiling**: Profile functions for execution time, disk writes, memory usage, network activity, and call counts using decorators.
- **Block and Line Profiling**: Profile specific code blocks or individual lines using context managers.
- **Visualization**: Generate a single PNG file with subplots for each metric, showing normalized values and raw data for easy comparison.
- **Customizable Metrics**: Configure which metrics to profile (e.g., write_bytes for disk, bytes_sent for network).
- **Logging Support**: Detailed logs of profiling stats with customizable log levels (e.g., INFO, DEBUG) or the ability to disable logging entirely.

## Installation
Install **SmartProfiler** via pip:
```bash
pip install smartprofiler
```

### Requirements:

Python 3.8 or higher
Dependencies: matplotlib, numpy, requests, psutil

## Usage Examples
SmartProfiler provides a unified interface through profiler classes (CPUProfiler, DiskProfiler, etc.) that can be used as decorators or context managers. Below are examples demonstrating how to use the library for profiling and visualization.

### 1. General Usage Examples

The following examples show how to use SmartProfiler to profile different aspects of your code, such as CPU usage, disk I/O, function calls, memory usage, and network I/O. These examples focus on logging the profiling results.

**1.1 Profiling a CPU-Intensive Function**

```bash
import time
from smartprofiler import CPUProfiler

# Initialize the CPU profiler
cpu_profiler = CPUProfiler(time_func='execution_time')

# Profile a CPU-intensive function
@cpu_profiler.profile_function
def compute_fibonacci(n):
    if n <= 1:
        return n
    return compute_fibonacci(n-1) + compute_fibonacci(n-2)

# Run the function
compute_fibonacci(20)

# Summarize statistics
cpu_profiler.summarize_stats()
```

**1.2 Profiling a Disk-Intensive Block**
```bash

from smartprofiler import DiskProfiler

# Initialize the Disk profiler
disk_profiler = DiskProfiler(disk_path='/tmp', disk_metrics={'write_bytes': True, 'disk_usage': False})

# Profile a disk-intensive block
with disk_profiler.profile_block("disk_write_block"):
    with open('/tmp/test_file.txt', 'w') as f:
        f.write("Sample data " * 1000)

# Summarize statistics
disk_profiler.summarize_stats()

```

**1.3 Profiling Network I/O with Logging Disabled**
```bash
import requests
from smartprofiler import NetworkProfiler

# Initialize the Network profiler with logging disabled
net_profiler = NetworkProfiler(network_metrics={'bytes_sent': True, 'bytes_recv': True}, enable_logging=False)

# Profile a network-intensive block
with net_profiler.profile_block("api_request"):
    requests.get('https://api.github.com')

# Manually print stats (since logging is disabled)
stats = net_profiler.get_stats()
print("Network stats:", stats)
```
See `examples/examples_general_usage.py` for more usage examples, including profiling function calls, memory usage, and multithreaded scenarios.

### 2. Visualization Examples

SmartProfiler can generate visualizations of profiling data using the plot_profiling_stats function. The following example demonstrates how to profile various tasks and visualize the results.

**2.1 Profiling and Visualizing CPU, Disk, and Memory Usage**

```bash
import time
import random
from smartprofiler import CPUProfiler, DiskProfiler, MemoryProfiler, plot_profiling_stats

# Initialize profilers
cpu_profiler = CPUProfiler(time_func='execution_time')
disk_profiler = DiskProfiler(disk_path='/tmp', disk_metrics={'write_bytes': True, 'disk_usage': False})
mem_profiler = MemoryProfiler()

# Profile a CPU-intensive function
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

# Run the function
matrix_multiply()

# Generate visualization
plot_profiling_stats(
    [cpu_profiler, disk_profiler, mem_profiler],
    output_dir='images',
    output_file='profiling_stats_cpu_disk_memory.png'
)
```

**Visualization Results**




1. CPU, Disk, and Memory Profiling: This visualization includes CPU-intensive tasks (matrix multiplication), disk I/O (writing large files), and memory usage (large list allocation).

 


2. Network and Function Call Profiling: This visualization highlights network I/O (multiple API requests) and function calls (recursive Fibonacci calculation).



See `examples/examples_visualization.py` for the complete visualization examples, which include additional scenarios like network I/O and function call profiling.

### 3. Multithreaded Profiling

SmartProfiler supports profiling in multithreaded environments. Here's an example:
```bash
import threading
from smartprofiler import CPUProfiler

cpu_profiler = CPUProfiler(time_func='execution_time')

def thread_function():
    with cpu_profiler.profile_block("thread_task"):
        time.sleep(1)

# Create and run threads
threads = [threading.Thread(target=thread_function) for _ in range(5)]
for t in threads:
    t.start()
for t in threads:
    t.join()

# Summarize stats
cpu_profiler.summarize_stats()
    
```

## Contributing to SmartProfiler
Contributions to **SmartProfiler** are welcome! Whether you're fixing a bug, adding a feature, or improving documentation, your help is appreciated.

### How to Contribute

1. **Fork the Repository**:  
    Start by forking the SmartProfiler repository.

2. **Make Your Changes**:  
    Make the necessary changes, whether it's fixing a bug, adding a new feature, or improving documentation.

3. **Submit a Pull Request**: 
    Once your changes are ready, submit a pull request with a clear description of what you've done. Be sure to include relevant details, such as any bugs fixed or features added.


### Code of Conduct
By contributing, you agree to follow the Code of Conduct, ensuring a positive environment for all.
License
SmartProfiler is licensed under the MIT License. See the LICENSE file for details.

**GitHub Repository**: [SmartProfiler on GitHub](https://github.com/vigsun19/quick_profile)
