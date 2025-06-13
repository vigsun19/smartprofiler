from smartprofiler.cpu_profiler import CPUProfiler
from smartprofiler.memory_profiler import MemoryProfiler
from smartprofiler.function_profiler import FunctionProfiler
from smartprofiler.export_stats import ExportStats

# Initialize profilers
cpu = CPUProfiler()
mem = MemoryProfiler()
func = FunctionProfiler()

# Profiled function
@cpu.profile_function
@mem.profile_function
@func.profile_function
def compute_fibonacci(n):
    if n <= 1:
        return n
    return compute_fibonacci(n - 1) + compute_fibonacci(n - 2)

print("Running compute_fibonacci(10)...")
compute_fibonacci(10)

# Export each profiler’s stats separately
cpu_exporter = ExportStats(cpu.get_stats())
mem_exporter = ExportStats(mem.get_stats())
func_exporter = ExportStats(func.get_stats())

cpu_exporter.export_stats("json", "examples/cpu_stats.json")
cpu_exporter.export_stats("csv", "examples/cpu_stats.csv")

mem_exporter.export_stats("json", "examples/mem_stats.json")
mem_exporter.export_stats("csv", "examples/mem_stats.csv")

func_exporter.export_stats("json", "examples/func_stats.json")
func_exporter.export_stats("csv", "examples/func_stats.csv")

print("Exported all profiler stats to individual files.")
