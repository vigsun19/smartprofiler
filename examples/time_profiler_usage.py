from smartprofiler.time import profile_time, profile_block, profile_line
import time
import threading

# Example function to demonstrate time profiling in a single-threaded environment
@profile_time
def time_function():
    print("Running time profiler...")
    time.sleep(2)  # Simulate a time-consuming task

# Example block to demonstrate block profiling for time in a single-threaded environment
def example_block():
    # Profiling a block of code for time
    with profile_block(profile_type='time'):
        print("Profiling a block of code for time...")
        time.sleep(1)  # Simulate a time-consuming block

# Example line profiling for time in a single-threaded environment
def example_line():
    # Profiling a specific line of code for time
    with profile_line(profile_type='time'):
        print("Profiling a line of code for time...")
        time.sleep(1)  # Simulate a delay in a specific line

# Multithreaded example for time profiling
def run_multithreaded_time_example():
    threads = []

    # Create and start threads for time profiling
    for i in range(5):  # Create 5 threads
        thread_name = f"Thread-{i + 1}"

        # Start a thread to run time profiling
        t_time = threading.Thread(target=time_function, args=())
        threads.append(t_time)
        t_time.start()

    # Wait for all threads to complete
    for t in threads:
        t.join()

if __name__ == '__main__':
    print("=== Single-threaded Time Profiling Example ===")
    time_function()
    example_block()
    example_line()

    print("\n=== Multithreaded Time Profiling Example ===")
    run_multithreaded_time_example()
