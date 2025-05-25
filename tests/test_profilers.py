import unittest
import time
import logging
import sys
import tracemalloc
from unittest.mock import patch, MagicMock
from smartprofiler import CPUProfiler, DiskProfiler, FunctionProfiler, MemoryProfiler, NetworkProfiler


class TestProfilers(unittest.TestCase):
    def setUp(self):
        # Configure logging to capture output for testing
        self.log_stream = MagicMock()
        self.logger = logging.getLogger('test_profilers')
        self.logger.setLevel(logging.DEBUG)  # Set to DEBUG to capture all levels
        # Remove any existing handlers to prevent interference
        self.logger.handlers = []
        handler = logging.StreamHandler(self.log_stream)
        handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(handler)

        # Initialize profilers with the test logger
        self.cpu_profiler = CPUProfiler(time_func='execution_time', logger=self.logger)
        self.disk_profiler = DiskProfiler(disk_path='/tmp', logger=self.logger)
        self.func_profiler = FunctionProfiler(logger=self.logger)
        self.mem_profiler = MemoryProfiler(logger=self.logger)
        self.net_profiler = NetworkProfiler(logger=self.logger)

    def tearDown(self):
        # Clear stats after each test
        self.cpu_profiler.clear_stats()
        self.disk_profiler.clear_stats()
        self.func_profiler.clear_stats()
        self.mem_profiler.clear_stats()
        self.net_profiler.clear_stats()
        # Clear logger handlers and reset log stream
        self.logger.handlers = []
        self.log_stream.reset_mock()

    def test_cpu_profiler_function(self):
        @self.cpu_profiler.profile_function
        def test_func():
            time.sleep(0.1)

        test_func()
        stats = self.cpu_profiler.get_stats()
        self.assertEqual(len(stats), 1)
        self.assertIn('execution_time', stats[0]['metrics'])
        self.assertGreater(stats[0]['metrics']['execution_time'], 0.09)  # Should be around 0.1s

    def test_cpu_profiler_block(self):
        with self.cpu_profiler.profile_block("test_block"):
            time.sleep(0.1)

        stats = self.cpu_profiler.get_stats()
        self.assertEqual(len(stats), 1)
        self.assertEqual(stats[0]['label'], "test_block")
        self.assertGreater(stats[0]['metrics']['execution_time'], 0.09)

    def test_cpu_profiler_line(self):
        with self.cpu_profiler.profile_line("test_line"):
            time.sleep(0.1)

        stats = self.cpu_profiler.get_stats()
        self.assertEqual(len(stats), 1)
        self.assertEqual(stats[0]['label'], "test_line")
        self.assertGreater(stats[0]['metrics']['execution_time'], 0.09)

    def test_cpu_profiler_summarize_stats(self):
        with self.cpu_profiler.profile_block("test_block"):
            time.sleep(0.1)

        self.cpu_profiler.summarize_stats()
        self.assertTrue(any("test_block" in call[0][0] for call in self.log_stream.write.call_args_list))

    @patch('builtins.open', new_callable=MagicMock)
    def test_disk_profiler_function(self, mock_open):
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file

        @self.disk_profiler.profile_function
        def test_func():
            with open('test.txt', 'w') as f:
                f.write("test data")

        test_func()
        stats = self.disk_profiler.get_stats()
        self.assertEqual(len(stats), 1)
        self.assertIn('write_bytes', stats[0]['metrics'])
        self.assertEqual(stats[0]['metrics']['write_bytes'], 0)  # Mocked, so no actual writes

    @patch('builtins.open', new_callable=MagicMock)
    def test_disk_profiler_block(self, mock_open):
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file

        with self.disk_profiler.profile_block("disk_block"):
            with open('test.txt', 'w') as f:
                f.write("test data")

        stats = self.disk_profiler.get_stats()
        self.assertEqual(len(stats), 1)
        self.assertEqual(stats[0]['label'], "disk_block")
        self.assertIn('write_bytes', stats[0]['metrics'])

    @patch('builtins.open', new_callable=MagicMock)
    def test_disk_profiler_line(self, mock_open):
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file

        with self.disk_profiler.profile_line("disk_line"):
            with open('test.txt', 'w') as f:
                f.write("test data")

        stats = self.disk_profiler.get_stats()
        self.assertEqual(len(stats), 1)
        self.assertEqual(stats[0]['label'], "disk_line")
        self.assertIn('write_bytes', stats[0]['metrics'])

    def test_disk_profiler_summarize_stats(self):
        with self.disk_profiler.profile_block("disk_block"):
            pass  # No actual disk I/O needed for this test

        self.disk_profiler.summarize_stats()
        self.assertTrue(any("disk_block" in call[0][0] for call in self.log_stream.write.call_args_list))

    def test_function_profiler_function(self):
        @self.func_profiler.profile_function
        def test_func():
            pass

        test_func()
        stats = self.func_profiler.get_stats()
        self.assertEqual(len(stats), 1)
        self.assertIn('call_count', stats[0]['metrics'])
        self.assertEqual(stats[0]['metrics']['call_count'], 1)

    def test_function_profiler_block(self):
        with self.func_profiler.profile_block("func_block"):
            def nested_func():
                pass

            nested_func()

        stats = self.func_profiler.get_stats()
        self.assertEqual(len(stats), 1)
        self.assertEqual(stats[0]['label'], "func_block")
        self.assertGreaterEqual(stats[0]['metrics']['call_count'], 1)

    def test_function_profiler_line(self):
        with self.func_profiler.profile_line("func_line"):
            def nested_func():
                pass

            nested_func()

        stats = self.func_profiler.get_stats()
        self.assertEqual(len(stats), 1)
        self.assertEqual(stats[0]['label'], "func_line")
        self.assertGreaterEqual(stats[0]['metrics']['call_count'], 1)

    def test_function_profiler_summarize_stats(self):
        with self.func_profiler.profile_block("func_block"):
            pass

        self.func_profiler.summarize_stats()
        self.assertTrue(any("func_block" in call[0][0] for call in self.log_stream.write.call_args_list))

    @patch('tracemalloc.get_traced_memory', return_value=(1000, 2000))
    @patch('tracemalloc.start')
    @patch('tracemalloc.stop')
    def test_memory_profiler_function(self, mock_stop, mock_start, mock_get_traced):
        @self.mem_profiler.profile_function
        def test_func():
            pass

        test_func()
        stats = self.mem_profiler.get_stats()
        self.assertEqual(len(stats), 1)
        self.assertIn('peak_mb', stats[0]['metrics'])
        self.assertAlmostEqual(stats[0]['metrics']['peak_mb'], 2000 / (1024 ** 2))

    @patch('tracemalloc.get_traced_memory', return_value=(1000, 2000))
    @patch('tracemalloc.start')
    @patch('tracemalloc.stop')
    def test_memory_profiler_block(self, mock_stop, mock_start, mock_get_traced):
        with self.mem_profiler.profile_block("mem_block"):
            pass

        stats = self.mem_profiler.get_stats()
        self.assertEqual(len(stats), 1)
        self.assertEqual(stats[0]['label'], "mem_block")
        self.assertIn('peak_mb', stats[0]['metrics'])

    @patch('tracemalloc.get_traced_memory', return_value=(1000, 2000))
    @patch('tracemalloc.start')
    @patch('tracemalloc.stop')
    def test_memory_profiler_line(self, mock_stop, mock_start, mock_get_traced):
        with self.mem_profiler.profile_line("mem_line"):
            pass

        stats = self.mem_profiler.get_stats()
        self.assertEqual(len(stats), 1)
        self.assertEqual(stats[0]['label'], "mem_line")
        self.assertIn('peak_mb', stats[0]['metrics'])

    def test_memory_profiler_summarize_stats(self):
        with self.mem_profiler.profile_block("mem_block"):
            pass

        self.mem_profiler.summarize_stats()
        self.assertTrue(any("mem_block" in call[0][0] for call in self.log_stream.write.call_args_list))

    @patch('smartprofiler.network_profiler.psutil.net_io_counters')
    def test_network_profiler_function(self, mock_net_io):
        mock_net_io.side_effect = [MagicMock(bytes_sent=1000, bytes_recv=2000),
                                   MagicMock(bytes_sent=1500, bytes_recv=2500)]

        @self.net_profiler.profile_function
        def test_func():
            pass

        test_func()
        stats = self.net_profiler.get_stats()
        self.assertEqual(len(stats), 1)
        self.assertIn('bytes_sent', stats[0]['metrics'])
        self.assertEqual(stats[0]['metrics']['bytes_sent'], 500)  # 1500 - 1000

    @patch('smartprofiler.network_profiler.psutil.net_io_counters')
    def test_network_profiler_block(self, mock_net_io):
        mock_net_io.side_effect = [MagicMock(bytes_sent=1000, bytes_recv=2000),
                                   MagicMock(bytes_sent=1500, bytes_recv=2500)]

        with self.net_profiler.profile_block("net_block"):
            pass

        stats = self.net_profiler.get_stats()
        self.assertEqual(len(stats), 1)
        self.assertEqual(stats[0]['label'], "net_block")
        self.assertIn('bytes_sent', stats[0]['metrics'])

    @patch('smartprofiler.network_profiler.psutil.net_io_counters')
    def test_network_profiler_line(self, mock_net_io):
        mock_net_io.side_effect = [MagicMock(bytes_sent=1000, bytes_recv=2000),
                                   MagicMock(bytes_sent=1500, bytes_recv=2500)]

        with self.net_profiler.profile_line("net_line"):
            pass

        stats = self.net_profiler.get_stats()
        self.assertEqual(len(stats), 1)
        self.assertEqual(stats[0]['label'], "net_line")
        self.assertIn('bytes_sent', stats[0]['metrics'])

    def test_network_profiler_summarize_stats(self):
        with self.net_profiler.profile_block("net_block"):
            pass

        self.net_profiler.summarize_stats()
        self.assertTrue(any("net_block" in call[0][0] for call in self.log_stream.write.call_args_list))

    @patch('smartprofiler.network_profiler.psutil.net_io_counters')
    def test_network_profiler_custom_log_level(self, mock_net_io):
        mock_net_io.side_effect = [MagicMock(bytes_sent=1000, bytes_recv=2000),
                                   MagicMock(bytes_sent=1500, bytes_recv=2500)]

        # Create a profiler with DEBUG log level
        debug_profiler = NetworkProfiler(logger=self.logger, log_level=logging.DEBUG)

        with debug_profiler.profile_block("debug_block"):
            pass

        # Check that the log message was written at DEBUG level
        self.assertTrue(any("debug_block" in call[0][0] for call in self.log_stream.write.call_args_list))

    @patch('smartprofiler.network_profiler.psutil.net_io_counters')
    def test_network_profiler_disable_logging(self, mock_net_io):
        mock_net_io.side_effect = [MagicMock(bytes_sent=1000, bytes_recv=2000),
                                   MagicMock(bytes_sent=1500, bytes_recv=2500)]

        # Create a profiler with logging disabled
        silent_profiler = NetworkProfiler(logger=self.logger, enable_logging=False)

        with silent_profiler.profile_block("silent_block"):
            pass

        silent_profiler.summarize_stats()

        # Check that no log messages were written
        self.assertFalse(self.log_stream.write.called, "No log messages should be written when enable_logging=False")

        # But stats should still be collected
        stats = silent_profiler.get_stats()
        self.assertEqual(len(stats), 1)
        self.assertIn('bytes_sent', stats[0]['metrics'])

    def test_cpu_profiler_custom_log_level(self):
        # Create a profiler with DEBUG log level
        debug_profiler = CPUProfiler(time_func='execution_time', logger=self.logger, log_level=logging.DEBUG)

        with debug_profiler.profile_block("debug_block"):
            time.sleep(0.1)

        # Check that the log message was written at DEBUG level
        self.assertTrue(any("debug_block" in call[0][0] for call in self.log_stream.write.call_args_list))

    def test_cpu_profiler_disable_logging(self):
        # Create a profiler with logging disabled
        silent_profiler = CPUProfiler(time_func='execution_time', logger=self.logger, enable_logging=False)

        with silent_profiler.profile_block("silent_block"):
            time.sleep(0.1)

        silent_profiler.summarize_stats()

        # Check that no log messages were written
        self.assertFalse(self.log_stream.write.called, "No log messages should be written when enable_logging=False")

        # But stats should still be collected
        stats = silent_profiler.get_stats()
        self.assertEqual(len(stats), 1)
        self.assertIn('execution_time', stats[0]['metrics'])


if __name__ == '__main__':
    unittest.main()
