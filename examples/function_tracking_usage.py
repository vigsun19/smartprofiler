from smartprofiler.function_tracking import profile_call_count
import time
import logging
import threading

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# --- Single-threaded Example Functions ---
@profile_call_count
def sample_function():
    """A simple function to demonstrate call count tracking."""
    logging.info("Executing sample function...")
    time.sleep(1)


@profile_call_count
def another_function():
    """Another function to demonstrate call count tracking."""
    logging.info("Executing another function...")
    time.sleep(0.5)


# --- Multithreaded Example Functions ---
@profile_call_count
def multithreaded_function(thread_name):
    """A simple function for multithreaded execution."""
    logging.info(f"{thread_name} executing...")
    time.sleep(1)


# Function to run the function across multiple threads
def run_multithreaded_example():
    threads = []

    # Create 5 threads, each calling the same function
    for i in range(5):
        thread_name = f"Thread-{i + 1}"
        thread = threading.Thread(target=multithreaded_function, args=(thread_name,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for t in threads:
        t.join()


# --- Main Script: Demonstrating Both Single and Multithreaded Examples ---
if __name__ == '__main__':
    print("=== Single-threaded Example ===")
    # Single-threaded function calls
    sample_function()
    sample_function()
    another_function()
    sample_function()

    print("\n--- Single-threaded function calls tracked above ---")

    print("\n=== Multithreaded Example ===")
    # Run the multithreaded example
    run_multithreaded_example()

    print("\n--- Multithreaded function calls tracked above ---")