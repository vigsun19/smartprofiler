from smartprofiler.cpu_time import profile_cpu_time, profile_block, profile_line
import time
import threading

# Example function to demonstrate CPU time profiling in a single-threaded environment
@profile_cpu_time
def cpu_time_function():
    print("Running CPU time profiler...")
    time.sleep(2)  # Simulate a time-consuming task

# Example block to demonstrate block profiling for CPU time in a single-threaded environment
def example_block():
    # Profiling a block of code for CPU time
    with profile_block(profile_type='cpu_time'):
        print("Profiling a block of code for CPU time...")
        time.sleep(1)  # Simulate a time-consuming block

# Example line profiling for CPU time in a single-threaded environment
def example_line():
    # Profiling a specific line of code for CPU time
    with profile_line(profile_type='cpu_time'):
        print("Profiling a line of code for CPU time...")
        time.sleep(1)  # Simulate a delay in a specific line

# Multithreaded example for CPU time profiling
def run_multithreaded_cpu_time_example():
    threads = []

    # Create and start threads for CPU time profiling
    for i in range(5):  # Create 5 threads
        thread_name = f"Thread-{i + 1}"

        # Start a thread to run CPU time profiling
        t_cpu_time = threading.Thread(target=cpu_time_function, args=())
        threads.append(t_cpu_time)
        t_cpu_time.start()

    # Wait for all threads to complete
    for t in threads:
        t.join()

if __name__ == '__main__':
    print("=== Single-threaded CPU Time Profiling Example ===")
    cpu_time_function()
    example_block()
    example_line()

    print("\n=== Multithreaded CPU Time Profiling Example ===")
    run_multithreaded_cpu_time_example()
