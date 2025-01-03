# SmartProfiler

SmartProfiler is a lightweight and easy-to-use Python library designed to help you effortlessly profile **execution time**, **memory usage**, **CPU time**, and **function call counts** in your Python code. Whether you're optimizing performance, debugging memory usage, tracking CPU utilization, or monitoring function calls, SmartProfiler provides a simple and efficient solution for all your profiling needs—especially in multithreaded environments.
## Why SmartProfiler?

- **Unified Profiling**: Unlike other libraries that focus on either time, memory, or CPU, SmartProfiler combines all four types of profiling into a single, intuitive tool. You can easily profile **time**, **memory**, **CPU**, and **function calls** with minimal setup.
- **Thread-Safe**: Designed with multithreaded applications in mind, SmartProfiler ensures that profiling works seamlessly across different threads without race conditions or conflicts.
- **Minimal Overhead**: The library introduces minimal performance overhead, providing accurate profiling data without slowing down your application.
- **Easy to Use**: Profiling functions, code blocks, and even specific lines of code is straightforward. You can use decorators or context managers with just a few lines of code.

## Features

- **Function-Level Profiling**: Profile execution time, memory usage, CPU time, and function call counts using decorators.
- **Code Block and Line Profiling**: Profile specific blocks or lines of code using context managers.
- **Multithreaded Profiling**: Profile functions, blocks, and lines in multithreaded environments with thread safety.
- **Flexible Logging**: Integration with Python's logging framework for detailed insights into your code's performance.
- **Function Call Tracking**: Track the number of times a function is called, thread-safe and efficient.

## Installation

You can easily install SmartProfiler via pip:

```bash
pip install smartprofiler

```

## Usage Examples
**Time Profiling for Functions**

```bash
from smartprofiler.time import profile_time

@profile_time
def my_function():
    time.sleep(1)  # Simulate a time-consuming task

```
**Memory Profiling for Functions**

```bash
from smartprofiler.memory import profile_memory

@profile_memory
def memory_intensive_function():
    data = [1] * (10**7)  # Simulate memory usage

```

**CPU Time Profiling for Functions**

```bash
from smartprofiler.cpu_time import profile_cpu_time

@profile_cpu_time
def cpu_intensive_function():
    # Simulate CPU-intensive task
    for _ in range(10**6):
        pass

```
**Disk Usage Profiling for Functions**

```bash
from smartprofiler.disk_usage import profile_method

@profile_method
def perform_disk_operations():
    """Simulate disk I/O by reading and writing data."""
    
    # Simulate writing to a file
    with open('example_file.txt', 'w') as f:
        f.write('Simulating disk I/O operations...')
    
    # Simulate reading from the file
    with open('example_file.txt', 'r') as f:
        content = f.read()

```
**Network Usage Profiling for Functions**

```bash
from smartprofiler.network_usage import profile_method

@profile_method
def fetch_data_from_api():
    """Simulate a network request."""
    import requests
    
    # Simulate a network request to an external API
    response = requests.get('https://www.example.com')
    print(f"Received {len(response.content)} bytes from {response.url}")

```
**Function Call Counting**

```bash
from smartprofiler.function_tracking import profile_call_count

@profile_call_count
def my_function():
    print("Function called")

my_function()  # Logs: Function 'my_function' has been called 1 times
my_function()  # Logs: Function 'my_function' has been called 2 times

```

**Block Profiling (Time, Memory & CPU-Usage)**

```bash
from smartprofiler.time import profile_block
from smartprofiler.memory import profile_block
from smartprofiler.cpu_time import profile_block

# Time Profiling Block
with profile_block('time'):
    time.sleep(1)

# Memory Profiling Block
with profile_block('memory'):
    data = [1] * (10**6)

# CPU Time Profiling Block
with profile_block('cpu_time'):
    # Simulate a CPU-intensive task
    for _ in range(10**6):
        pass

```

**Line Profiling (Time, Memory & CPU-Usage)**

```bash
from smartprofiler.time import profile_line
from smartprofiler.memory import profile_line
from smartprofiler.cpu_time import profile_line

# Time Profiling Line
with profile_line('time'):
    result = sum([i for i in range(1000)])

# Memory Profiling Line
with profile_line('memory'):
    data = [1] * (10**6)

# CPU Time Profiling Line
with profile_line('cpu_time'):
    # Simulate CPU-intensive line
    for _ in range(10**6):
        pass

```

**Multithreaded Profiling**

```bash
import threading
from smartprofiler.time import profile_time

def thread_function():
    with profile_time:
        time.sleep(1)

threads = [threading.Thread(target=thread_function) for _ in range(5)]
for t in threads:
    t.start()
for t in threads:
    t.join()

```
## Contributing to SmartProfiler
Contributions to **SmartProfiler** are welcome! Whether you're fixing a bug, adding a feature, or improving documentation, your help is appreciated.


### How to Contribute

1. **Fork the Repository**:  
   Start by forking the [SmartProfiler repository](https://github.com/vigsun19/quick_profile).

2. **Make Your Changes**:  
   Make the necessary changes, whether it's fixing a bug, adding a new feature, or improving documentation.

3. **Submit a Pull Request**:  
   Once your changes are ready, submit a pull request with a clear description of what you've done. Be sure to include relevant details, such as any bugs fixed or features added.

### Code of Conduct

By contributing, you agree to follow the Code of Conduct, ensuring a positive environment for all.

---

**GitHub Repository**: [SmartProfiler on GitHub](https://github.com/vigsun19/quick_profile)
