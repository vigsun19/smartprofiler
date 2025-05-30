from base_profiler_export_test import ExportableProfiler

# Create an instance
profiler = ExportableProfiler()

# Add some fake stats manually
profiler.stats = [
    {"label": "load_data", "metrics": {"execution_time": 0.12, "memory_used": 32}},
    {"label": "clean_data", "metrics": {"execution_time": 0.25, "memory_used": 54}}
]

# Export to JSON
profiler.export_stats(format='json', file_path='exported_stats.json')
print("Exported to exported_stats.json")

# Export to CSV
profiler.export_stats(format='csv', file_path='exported_stats.csv')
print("Exported to exported_stats.csv")
