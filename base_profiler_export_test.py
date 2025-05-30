import logging
from smartprofiler.base_profiler import BaseProfiler
import json
import csv

class ExportableProfiler(BaseProfiler):
    def profile_function(self, func):
        return func  # Dummy implementation for testing

    def profile_block(self, label: str):
        pass  # Not needed for export test

    def profile_line(self, label: str):
        pass  # Not needed for export test

    def export_stats(self, format: str, file_path: str):
        if format not in ['json', 'csv']:
            raise ValueError("Format must be either 'json' or 'csv'")

        if format == 'json':
            with open(file_path, 'w') as f:
                json.dump(self.stats, f, indent=4)

        elif format == 'csv':
            if not self.stats:
                raise ValueError("No stats available to export")

            first_metrics = list(self.stats[0].get("metrics", {}).keys())
            headers = ['label'] + first_metrics

            with open(file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                for item in self.stats:
                    row = [item.get('label', '')] + [item['metrics'].get(k, '') for k in first_metrics]
                    writer.writerow(row)
