import unittest
import threading

# Assuming the decorator is in a module named 'function_tracking.py'
from smartprofiler.function_tracking import profile_call_count

class TestCallCountProfiler(unittest.TestCase):

    def test_profile_call_count(self):
        """Test the profile_call_count decorator."""
        # Define a simple function to apply the decorator to
        @profile_call_count
        def test_function():
            return "Hello, World!"

        # Call the decorated function multiple times
        with self.assertLogs(level='INFO') as log:
            test_function()
            test_function()

        # Verify that the call count was logged correctly
        log_output = log.output
        self.assertIn("Function 'test_function' has been called 1 times", log_output[0])
        self.assertIn("Function 'test_function' has been called 2 times", log_output[1])

    def test_profile_call_count_multiple_calls(self):
        """Test that call count increments correctly for multiple calls."""
        # Define the function
        @profile_call_count
        def test_function():
            return "Test"

        # Call it multiple times
        with self.assertLogs(level='INFO') as log:
            for _ in range(5):
                test_function()

        # Check if the call count was logged properly
        log_output = log.output
        self.assertIn("Function 'test_function' has been called 5 times", log_output[-1])

    def test_profile_call_count_thread_safety(self):
        """Test that the call count is thread-safe."""
        # Define the function
        @profile_call_count
        def test_function():
            return "Test"

        # Use threads to call the function concurrently
        def thread_function():
            for _ in range(3):
                test_function()

        threads = [threading.Thread(target=thread_function) for _ in range(3)]

        with self.assertLogs(level='INFO') as log:
            # Start the threads
            for thread in threads:
                thread.start()

            # Wait for them to finish
            for thread in threads:
                thread.join()

        # Check if the function was called the correct number of times
        log_output = log.output
        self.assertIn("Function 'test_function' has been called 9 times", log_output[-1])


if __name__ == "__main__":
    unittest.main()
