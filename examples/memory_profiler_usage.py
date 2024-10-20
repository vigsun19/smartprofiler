from smartprofiler.memory import profile_memory, profile_block, profile_line
import threading

# Example function to demonstrate memory profiling in a single-threaded environment
@profile_memory
def memory_function():
    print("Running memory profiler...")
    x = [1] * (10 ** 7)  # Simulate memory usage

# Example block to demonstrate block profiling for memory in a single-threaded environment
def example_block():
    # Profiling a block of code for memory
    with profile_block(profile_type='memory'):
        print("Profiling a block of code for memory...")
        _ = [1] * (10 ** 6)  # Simulate memory usage

# Example line profiling for memory in a single-threaded environment
def example_line():
    # Profiling a specific line of code for memory
    with profile_line(profile_type='memory'):
        print("Profiling a line of code for memory...")
        _ = [1] * (10 ** 6)  # Simulate memory usage in a specific line

# Multithreaded example for memory profiling
def run_multithreaded_memory_example():
    threads = []

    # Create and start threads for memory profiling
    for i in range(5):  # Create 5 threads
        thread_name = f"Thread-{i + 1}"

        # Start a thread to run memory profiling
        t_memory = threading.Thread(target=memory_function, args=())
        threads.append(t_memory)
        t_memory.start()

    # Wait for all threads to complete
    for t in threads:
        t.join()

if __name__ == '__main__':
    print("=== Single-threaded Memory Profiling Example ===")
    memory_function()
    example_block()
    example_line()

    print("\n=== Multithreaded Memory Profiling Example ===")
    run_multithreaded_memory_example()
