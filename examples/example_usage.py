from smartprofiler import profile_time, profile_block, profile_line, profile_memory
import time
import threading


# Example function to demonstrate time profiling in a single-threaded environment
@profile_time
def time_function():
    print("Running time profiler...")
    time.sleep(2)  # Simulate a time-consuming task


# Example function to demonstrate memory profiling in a single-threaded environment
@profile_memory
def memory_function():
    print("Running memory profiler...")
    x = [1] * (10 ** 7)  # Simulate memory usage


# Example block to demonstrate block profiling in a single-threaded environment
def example_block():
    # Profiling a block of code for time
    with profile_block(profile_type='time'):
        print("Profiling a block of code for time...")
        time.sleep(1)  # Simulate a time-consuming block

    # Profiling a block of code for memory
    with profile_block(profile_type='memory'):
        print("Profiling a block of code for memory...")
        _ = [1] * (10 ** 6)  # Simulate memory usage


# Example line profiling in a single-threaded environment
def example_line():
    # Profiling a specific line of code for time
    with profile_line(profile_type='time'):
        print("Profiling a line of code for time...")
        time.sleep(1)  # Simulate a delay in a specific line

    # Profiling a specific line of code for memory
    with profile_line(profile_type='memory'):
        print("Profiling a line of code for memory...")
        _ = [1] * (10 ** 6)  # Simulate memory usage in a specific line


# Example function to demonstrate time profiling in a multithreaded environment
@profile_time
def time_function_in_thread(thread_name):
    print(f"Thread {thread_name}: Running time profiler...")
    time.sleep(2)  # Simulate a time-consuming task


# Example function to demonstrate memory profiling in a multithreaded environment
@profile_memory
def memory_function_in_thread(thread_name):
    print(f"Thread {thread_name}: Running memory profiler...")
    x = [1] * (10 ** 7)  # Simulate memory usage


# Example block to demonstrate block profiling in a multithreaded environment
def example_block_in_thread(thread_name):
    print(f"Thread {thread_name}: Profiling a block of code for time...")
    with profile_block(profile_type='time'):
        time.sleep(1)  # Simulate a time-consuming block

    print(f"Thread {thread_name}: Profiling a block of code for memory...")
    with profile_block(profile_type='memory'):
        _ = [1] * (10 ** 6)  # Simulate memory usage


# Example line profiling in a multithreaded environment
def example_line_in_thread(thread_name):
    print(f"Thread {thread_name}: Profiling a line of code for time...")
    with profile_line(profile_type='time'):
        time.sleep(1)  # Simulate a delay in a specific line

    print(f"Thread {thread_name}: Profiling a line of code for memory...")
    with profile_line(profile_type='memory'):
        _ = [1] * (10 ** 6)  # Simulate memory usage in a specific line


# Function to simulate multiple threads running concurrently
def run_multithreaded_example():
    threads = []

    # Create and start threads
    for i in range(5):  # Create 5 threads
        thread_name = f"Thread-{i + 1}"

        # Start a thread to run time profiling
        t_time = threading.Thread(target=time_function_in_thread, args=(thread_name,))
        threads.append(t_time)
        t_time.start()

        # Start a thread to run memory profiling
        t_memory = threading.Thread(target=memory_function_in_thread, args=(thread_name,))
        threads.append(t_memory)
        t_memory.start()

        # Start a thread to profile code block
        t_block = threading.Thread(target=example_block_in_thread, args=(thread_name,))
        threads.append(t_block)
        t_block.start()

        # Start a thread to profile specific lines of code
        t_line = threading.Thread(target=example_line_in_thread, args=(thread_name,))
        threads.append(t_line)
        t_line.start()

    # Wait for all threads to complete
    for t in threads:
        t.join()


if __name__ == '__main__':
    # Test the functions in a single-threaded environment
    print("=== Single-threaded Example ===")
    time_function()
    memory_function()
    example_block()
    example_line()

    # Run multithreaded profiling example
    print("\n=== Multithreaded Example ===")
    run_multithreaded_example()
