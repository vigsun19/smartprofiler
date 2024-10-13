import time
import unittest
import threading
import logging
from smartprofiler import profile_time, profile_block, profile_line, profile_memory

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class TestSmartProfiler(unittest.TestCase):

    def test_example_function(self):
        """Test the time profiling of a function."""

        @profile_time
        def dummy_function():
            time.sleep(1)  # Sleep to simulate some processing time

        # Capture logs using assertLogs
        with self.assertLogs(level='INFO') as log:
            dummy_function()

        # Check if the expected log message is in the captured logs
        log_message = log.output[0]
        self.assertIn("Function 'dummy_function' took", log_message)
        self.assertIn("seconds", log_message)

    def test_block_profiling(self):
        """Test block profiling."""
        with self.assertLogs(level='INFO') as log:
            with profile_block():
                time.sleep(0.5)  # Sleep to simulate some processing time inside the block

        # Check if the expected log message is in the captured logs
        log_message = log.output[0]
        self.assertIn("Code block took", log_message)
        self.assertIn("seconds", log_message)

    def test_line_profiling(self):
        """Test line profiling."""
        with self.assertLogs(level='INFO') as log:
            with profile_line():
                total = sum(i for i in range(1000))  # Perform a simple computation

        # Check if the expected log message is in the captured logs
        log_message = log.output[0]
        self.assertIn("Line(s) took", log_message)
        self.assertIn("seconds", log_message)

    def test_memory_function(self):
        """Test the memory profiling of a function."""

        @profile_memory
        def memory_intensive_function():
            time.sleep(1)
            data = [1] * (10 ** 6)  # Simulate some memory usage

        # Capture logs using assertLogs
        with self.assertLogs(level='INFO') as log:
            memory_intensive_function()

        # Check if the expected log message is in the captured logs
        log_message = log.output[0]
        self.assertIn("Function 'memory_intensive_function' used", log_message)
        self.assertIn("KB of memory", log_message)

    def test_block_memory_profiling(self):
        """Test block memory profiling."""
        with self.assertLogs(level='INFO') as log:
            with profile_block('memory'):
                data = [1] * (10 ** 6)  # Simulate memory usage inside the block

        # Check if the expected log message is in the captured logs
        log_message = log.output[0]
        self.assertIn("Code block used", log_message)
        self.assertIn("KB of memory", log_message)


    def test_invalid_profile_type(self):
        """Test for invalid profile_type handling in context managers."""
        with self.assertRaises(ValueError):
            with profile_block('invalid_type'):
                pass

    def test_empty_code_block(self):
        """Test an empty code block to ensure no errors occur."""
        with self.assertLogs(level='INFO') as log:
            with profile_block():
                pass  # Empty block

        log_message = log.output[0]
        self.assertIn("Code block took", log_message)
        self.assertIn("seconds", log_message)

    def test_logging_level(self):
        """Test logging at different levels (INFO and DEBUG)."""

        @profile_time
        def simple_function():
            time.sleep(0.5)

        # Change logging level to DEBUG
        logging.basicConfig(level=logging.DEBUG)

        with self.assertLogs(level='DEBUG') as log:
            simple_function()

        self.assertIn("Function 'simple_function' took", log.output[0])


if __name__ == '__main__':
    unittest.main()
