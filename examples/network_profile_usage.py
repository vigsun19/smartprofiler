import time
from smartprofiler.network_usage import profile_block, profile_method


# Example of Method-Level Profiling with the Decorator
@profile_method
def simulate_network_activity():
    """Simulate network activity by waiting (no actual request)."""
    print("Starting network simulation...")

    # Simulate network activity (mocked by sleep)
    time.sleep(2)  # Simulate time taken by network activity

    print("Network simulation complete.")


# Call the method (this will trigger the network profiling)
simulate_network_activity()


# Example of Block-Level Profiling with the Context Manager
def perform_network_operations():
    """Simulate multiple network operations inside a code block."""
    with profile_block():
        print("Starting network operations block...")

        # Simulate network activity (mocked by sleep)
        time.sleep(1)  # Simulate a file download or some network request

        print("Simulated download completed.")

        time.sleep(1)  # Simulate another network operation like an upload
        print("Simulated upload completed.")

        print("Network operations block complete.")


# Run the network operations (this will trigger the block-level profiling)
perform_network_operations()