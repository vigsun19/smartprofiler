from smartprofiler.export_stats import ExportStats

profiler = ExportStats()
profiler.stats = [
    {"label": "load_data", "metrics": {"execution_time": 0.25, "memory": 50}}
]
profiler.export_stats(format='json', file_path='examples/example_output.json')
profiler.export_stats(format='csv', file_path='examples/example_output.csv')
print("✅ Example export completed. Files saved as 'example_output.json' and 'example_output.csv'")
