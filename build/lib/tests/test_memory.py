import unittest
import time
from smartprofiler.memory import profile_memory, profile_block, profile_line

class TestMemoryProfiler(unittest.TestCase):

    def test_profile_memory_decorator(self):
        """Test the profile_memory decorator."""

        # Define a function to test the memory decorator
        @profile_memory
        def test_function():
            # Simulate memory usage
            data = [1] * (10**6)  # Allocate memory
            time.sleep(0.1)  # Simulate some work
            return data

        # Call the decorated function
        with self.assertLogs(level='INFO') as log:
            test_function()

        # Ensure memory logging occurs and check the log message
        log_output = log.output[0]
        self.assertIn("Function 'test_function' used", log_output)
        self.assertIn("KB of memory (peak)", log_output)

    def test_profile_block(self):
        """Test the profile_block context manager."""
        # Use the context manager to profile a block of code
        with profile_block(profile_type='memory'):
            # Simulate memory usage
            data = [1] * (10**6)  # Allocate memory
            time.sleep(0.1)  # Simulate some work

        # Check the logs
        with self.assertLogs(level='INFO') as log:
            with profile_block(profile_type='memory'):
                pass

        log_output = log.output[0]
        self.assertIn("Code block used", log_output)
        self.assertIn("KB of memory (peak)", log_output)

    def test_profile_line(self):
        """Test the profile_line context manager."""

        # Use the context manager to profile a specific line of code
        with profile_line(profile_type='memory'):
            # Simulate memory usage
            data = [1] * (10**6)  # Allocate memory
            time.sleep(0.1)  # Simulate some work

        # Check the logs
        with self.assertLogs(level='INFO') as log:
            with profile_line(profile_type='memory'):
                pass

        log_output = log.output[0]
        self.assertIn("Line(s) used", log_output)
        self.assertIn("KB of memory (peak)", log_output)

    def test_profile_block_invalid_type(self):
        """Test the profile_block context manager with an invalid profile_type."""
        with self.assertRaises(ValueError):
            with profile_block(profile_type='invalid_type'):
                pass

    def test_profile_line_invalid_type(self):
        """Test the profile_line context manager with an invalid profile_type."""
        with self.assertRaises(ValueError):
            with profile_line(profile_type='invalid_type'):
                pass

if __name__ == "__main__":
    unittest.main()
