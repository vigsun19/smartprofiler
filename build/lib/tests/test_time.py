import unittest
from unittest import mock
from smartprofiler.time import profile_time, profile_block, profile_line
import time


class TimeProfilerTests(unittest.TestCase):

    @mock.patch('smartprofiler.time.logging.info')  # Mocking logging.info
    @mock.patch('time.perf_counter')  # Corrected the mock for time.perf_counter
    def test_profile_time_decorator(self, mock_time, mock_log):
        """Test the profile_time decorator."""

        # Simulate the start and end times
        mock_time.side_effect = [1.0, 2.0]  # Function should take 1 second

        # Define a simple function to apply the decorator to
        @profile_time
        def test_function():
            time.sleep(0.5)  # Simulate work

        # Call the decorated function
        test_function()

        # Verify that the logging.info function was called to log execution time
        mock_log.assert_called_with("Function 'test_function' took 1.0000 seconds")

    @mock.patch('smartprofiler.time.logging.info')  # Mocking logging.info
    @mock.patch('time.perf_counter')  # Corrected the mock for time.perf_counter
    def test_profile_block(self, mock_time, mock_log):
        """Test the profile_block context manager."""

        # Simulate the start and end times for the block
        mock_time.side_effect = [1.0, 2.0]  # Block should take 1 second

        # Use the context manager
        with profile_block(profile_type='time'):
            time.sleep(0.5)  # Simulate work

        # Verify that the logging.info function was called to log execution time
        mock_log.assert_called_with("Code block took 1.0000 seconds")

    @mock.patch('smartprofiler.time.logging.info')  # Mocking logging.info
    @mock.patch('time.perf_counter')  # Corrected the mock for time.perf_counter
    def test_profile_line(self, mock_time, mock_log):
        """Test the profile_line context manager."""

        # Simulate the start and end times for the line
        mock_time.side_effect = [1.0, 1.5]  # Line should take 0.5 seconds

        # Use the context manager
        with profile_line(profile_type='time'):
            time.sleep(0.5)  # Simulate work on a line

        # Verify that the logging.info function was called to log execution time
        mock_log.assert_called_with("Line(s) took 0.5000 seconds")

    @mock.patch('smartprofiler.time.logging.error')  # Mocking logging.error for invalid profile_type
    @mock.patch('time.perf_counter')  # Corrected the mock for time.perf_counter
    def test_profile_block_invalid_type(self, mock_time, mock_error):
        """Test the profile_block context manager with an invalid profile_type."""

        # Attempt to use the context manager with an invalid profile_type
        with self.assertRaises(ValueError):
            with profile_block(profile_type='invalid_type'):
                pass

        # Verify that an error was logged when an invalid profile_type is used
        mock_error.assert_called_with("Unknown profile_type: 'invalid_type', use 'time'")

    @mock.patch('smartprofiler.time.logging.error')  # Mocking logging.error for invalid profile_type
    @mock.patch('time.perf_counter')  # Corrected the mock for time.perf_counter
    def test_profile_line_invalid_type(self, mock_time, mock_error):
        """Test the profile_line context manager with an invalid profile_type."""

        # Attempt to use the context manager with an invalid profile_type
        with self.assertRaises(ValueError):
            with profile_line(profile_type='invalid_type'):
                pass

        # Verify that an error was logged when an invalid profile_type is used
        mock_error.assert_called_with("Unknown profile_type: 'invalid_type', use 'time'")

# Run the tests
if __name__ == "__main__":
    unittest.main()
