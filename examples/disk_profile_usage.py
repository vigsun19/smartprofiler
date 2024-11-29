import time
from smartprofiler.disk_usage import profile_block, profile_method

# Example function to simulate multiple disk I/O operations
def perform_disk_operations():
    """Simulate multiple disk I/O operations inside a code block."""
    with profile_block():
        # Simulate writing to files in a loop
        for i in range(5):
            with open(f'example_file_{i}.txt', 'w') as f:
                f.write(f"This is file number {i}")
            time.sleep(0.1)  # Simulate some delay

# Run the disk I/O operations
perform_disk_operations()

# Example method to simulate disk usage
@profile_method
def write_to_file():
    """Simulate writing to a file and performing some disk I/O."""
    with open('example_file.txt', 'w') as f:
        f.write('This is a test file. Just simulating some disk I/O operations.')
    # Simulate additional disk usage by appending more data
    with open('example_file.txt', 'a') as f:
        f.write('\nAppending some more data to the file.')
    time.sleep(1)  # Simulate some delay to observe disk usage over time

# Call the method
write_to_file()