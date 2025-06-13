import os
import json
import csv
import unittest

from smartprofiler.cpu_profiler import CPUProfiler
from smartprofiler.disk_profiler import DiskProfiler
from smartprofiler.function_profiler import FunctionProfiler
from smartprofiler.memory_profiler import MemoryProfiler
from smartprofiler.network_profiler import NetworkProfiler
from smartprofiler.export_stats import ExportStats


class TestExporter(unittest.TestCase):
    def setUp(self):
        self.cpu = CPUProfiler()
        self.mem = MemoryProfiler()
        self.disk = DiskProfiler(disk_path=r"C:\Windows\Temp")
        self.func = FunctionProfiler()
        self.net = NetworkProfiler()

        @self.cpu.profile_function
        @self.mem.profile_function
        @self.disk.profile_function
        @self.func.profile_function
        @self.net.profile_function
        def work():
            return [i ** 2 for i in range(1000)]

        work()

        self.profilers = {
            "cpu": self.cpu,
            "mem": self.mem,
            "disk": self.disk,
            "func": self.func,
            "net": self.net,
        }

    def tearDown(self):
        for ext in ("json", "csv"):
            for name in self.profilers:
                f = f"{name}_stats.{ext}"
                if os.path.exists(f):
                    os.remove(f)

    def test_export_json(self):
        for name, profiler in self.profilers.items():
            output = f"{name}_stats.json"
            stats = profiler.get_stats()
            ExportStats(stats).export_stats("json", output)
            self.assertTrue(os.path.exists(output))
            with open(output) as f:
                data = json.load(f)
            self.assertIsInstance(data, list)
            self.assertTrue(len(data) > 0)

    def test_export_csv(self):
        for name, profiler in self.profilers.items():
            output = f"{name}_stats.csv"
            stats = profiler.get_stats()
            ExportStats(stats).export_stats("csv", output)
            self.assertTrue(os.path.exists(output))
            with open(output) as f:
                reader = csv.DictReader(f)
                rows = list(reader)
            self.assertTrue(len(rows) > 0)


if __name__ == "__main__":
    unittest.main()
