import unittest
import os
import json
import csv
import sys

# Add parent directory to import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from smartprofiler.export_stats import ExportStats

class TestExportStats(unittest.TestCase):

    def test_export_to_json(self):
        profiler = ExportStats()
        profiler.stats = [
            {"label": "load_data", "metrics": {"execution_time": 0.5, "memory": 100}}
        ]
        file_path = "test_stats.json"
        profiler.export_stats(format='json', file_path=file_path)

        self.assertTrue(os.path.exists(file_path))
        with open(file_path, "r") as f:
            data = json.load(f)
            self.assertEqual(data[0]["label"], "load_data")
            self.assertEqual(data[0]["metrics"]["execution_time"], 0.5)

        os.remove(file_path)

    def test_export_to_csv(self):
        profiler = ExportStats()
        profiler.stats = [
            {"label": "load_data", "metrics": {"execution_time": 0.5, "memory": 100}}
        ]
        file_path = "test_stats.csv"
        profiler.export_stats(format='csv', file_path=file_path)

        self.assertTrue(os.path.exists(file_path))
        with open(file_path, "r") as f:
            reader = csv.reader(f)
            rows = list(reader)
            self.assertEqual(rows[0], ['label', 'execution_time', 'memory'])
            self.assertEqual(rows[1][0], 'load_data')
            self.assertAlmostEqual(float(rows[1][1]), 0.5)

        os.remove(file_path)


if __name__ == '__main__':
    unittest.main()
