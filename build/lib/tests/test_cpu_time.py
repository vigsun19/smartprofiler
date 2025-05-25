import unittest
import time
from smartprofiler.cpu_time import profile_cpu_time, profile_block, profile_line

class TestCPUTimeProfiler(unittest.TestCase):

    def test_profile_cpu_time_decorator(self):
        """Test the profile_cpu_time decorator."""
        # Define a function to test the CPU time decorator
        @profile_cpu_time
        def test_function():
            # Simulate CPU work
            time.sleep(0.1)  # Simulate a small delay

        # Call the decorated function
        with self.assertLogs(level='INFO') as log:
            test_function()

        # Ensure that the CPU time logging occurred
        log_output = log.output[0]
        self.assertIn("Function 'test_function' used", log_output)
        self.assertIn("seconds of CPU time", log_output)

    def test_profile_block(self):
        """Test the profile_block context manager."""
        # Use the context manager to profile a block of code
        with profile_block(profile_type='cpu_time'):
            # Simulate CPU work
            time.sleep(0.1)  # Simulate a small delay

        # Check the logs
        with self.assertLogs(level='INFO') as log:
            with profile_block(profile_type='cpu_time'):
                pass

        log_output = log.output[0]
        self.assertIn("Code block took", log_output)
        self.assertIn("seconds of CPU time", log_output)

    def test_profile_line(self):
        """Test the profile_line context manager."""

        # Use the context manager to profile a specific line of code
        with profile_line(profile_type='cpu_time'):
            # Simulate CPU work
            time.sleep(0.1)  # Simulate a small delay

        # Check the logs
        with self.assertLogs(level='INFO') as log:
            with profile_line(profile_type='cpu_time'):
                pass

        log_output = log.output[0]
        self.assertIn("Line(s) took", log_output)
        self.assertIn("seconds of CPU time", log_output)

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
