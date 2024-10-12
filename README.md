# QuickProfile

A simple profiling library to measure execution time for functions, code blocks, and specific lines of code.

## Features

- **Function Profiling**: Decorate functions to log their execution time.
- **Block Profiling**: Use a context manager to profile a block of code.
- **Line Profiling**: Measure the execution time of specific lines of code.

## Installation

You can install QuickProfile directly from the source code or via PyPI:

### From PyPI

To install the latest version from PyPI, use:

```bash
pip install quickprofile

```

## Usage
**Profiling a Function:**
Use the `@profile_time` decorator to measure the execution time of a function:

```bash
from quickprofile import profile_time
import time

@profile_time
def my_function():
    # Simulate a time-consuming task
    time.sleep(1)

my_function()  # Logs the execution time

```

**Profiling a Code Block:**
Use the `profile_block` context manager to measure the execution time of a block of code:
```bash
from quickprofile import profile_block
import time

with profile_block():
    # Simulate a time-consuming task
    time.sleep(2)  # This will be logged

```

**Profiling Specific Lines:**
Use the `profile_line` context manager to measure the execution time of specific lines:
```bash
from quickprofile import profile_line

with profile_line():
    total = sum(i for i in range(1000000))  # This line's execution time will be logged


```