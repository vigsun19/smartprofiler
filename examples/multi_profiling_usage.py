from smartprofiler.time import profile_time
from smartprofiler.memory import profile_memory
from smartprofiler.cpu_time import profile_cpu_time
from smartprofiler.function_tracking import profile_call_count
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Example function using all four decorators
@profile_time
@profile_memory
@profile_cpu_time
@profile_call_count
def example_function():
    """Example function that performs some work to demonstrate profiling."""
    logging.info("Starting example function...")
    time.sleep(2)  # Simulate a time-consuming task
    # Simulate memory usage
    data = [1] * (10 ** 6)
    logging.info("Finished example function.")

# --- Running the Example ---
if __name__ == "__main__":
    logging.info("=== Executing example function (single execution) ===")
    example_function()

    logging.info("\n=== Executing example function (multiple executions) ===")
    example_function()
    example_function()
