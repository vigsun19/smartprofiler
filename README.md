# SmartProfiler

SmartProfiler is a lightweight and easy-to-use Python library designed to help you effortlessly profile both the execution time and memory usage of your Python code. Whether you're optimizing performance, debugging memory usage, or profiling applications running in multithreaded environments, SmartProfiler offers a clean and efficient solution.
## Why SmartProfiler?

- **Unified Profiling**: Unlike other libraries that focus on either time or memory, SmartProfiler provides simple and intuitive decorators and context managers to profile both time and memory usage.
- **Thread-Safe**: Specifically designed to support multithreaded applications, ensuring that profiling works seamlessly across different threads without race conditions or conflicts.
- **Minimal Overhead**: The library is designed to introduce minimal performance overhead, so you can get accurate measurements without complicating your workflow.
- **Easy to Use**: With just a few lines of code, you can start profiling functions, blocks of code, or even specific lines with just decorators and context managers.
## Features

- **Function-Level Profiling**: Profile execution time or memory usage using decorators.
- **Code Block and Line Profiling**: Profile specific blocks or lines of code using context managers.
- **Multithreaded Profiling**: Profile functions, blocks, and lines in multithreaded environments with thread safety.
- **Flexible Logging**: Integration with Python's logging framework for detailed insights into your code's performance.

## Installation

You can easily install SmartProfiler via pip:

```bash
pip install smartprofiler

```

## Usage Examples
**Time Profiling for Functions**

```bash
from smartprofiler import profile_time

@profile_time
def my_function():
    time.sleep(1)  # Simulate a time-consuming task

```
**Memory Profiling for Functions**

```bash
from smartprofiler import profile_memory

@profile_memory
def memory_intensive_function():
    data = [1] * (10**7)  # Simulate memory usage

```
**Block Profiling (Time & Memory)**

```bash
from smartprofiler import profile_block

with profile_block('time'):
    time.sleep(1)

with profile_block('memory'):
    data = [1] * (10**6)

```

**Line Profiling (Time & Memory)**

```bash
from smartprofiler import profile_line

with profile_line('time'):
    result = sum([i for i in range(1000)])

with profile_line('memory'):
    data = [1] * (10**6)

```

**Multithreaded Profiling**

```bash
import threading
from smartprofiler import profile_time

def thread_function():
    with profile_time:
        time.sleep(1)

threads = [threading.Thread(target=thread_function) for _ in range(5)]
for t in threads:
    t.start()
for t in threads:
    t.join()

```
