import os  
import json
import csv
from smartprofiler.base_profiler import BaseProfiler

class ExportStats(BaseProfiler):
    def __init__(self, stats, logger=None, log_level=None, enable_logging=True):
        super().__init__(logger=logger, log_level=log_level or 20, enable_logging=enable_logging)
        self.stats = stats  # Save the list of profiling data

    def profile_function(self, func):
        return func  # Not used here, but kept for compatibility

    def profile_block(self, label: str):
        pass  # Placeholder for block profiling

    def profile_line(self, label: str):
        pass  # Placeholder for line profiling

    def export_stats(self, format: str, file_path: str):
        if format not in ['json', 'csv']:
            raise ValueError("Format must be either 'json' or 'csv'")

        # Make sure the target directory exists
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        # Export as JSON (pretty-printed)
        if format == 'json':
            with open(file_path, 'w') as f:
                json.dump(self.stats, f, indent=4)

        # Export as CSV (table format)
        elif format == 'csv':
            if not self.stats:
                raise ValueError("No stats available to export")

            # Grab metric names from the first item
            first_metrics = list(self.stats[0].get("metrics", {}).keys())
            headers = ['label'] + first_metrics

            with open(file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                for item in self.stats:
                    row = [item.get('label', '')] + [item['metrics'].get(k, '') for k in first_metrics]
                    writer.writerow(row)
