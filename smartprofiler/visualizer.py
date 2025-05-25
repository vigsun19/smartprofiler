import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict
import os
import math


def plot_profiling_stats(
        profilers: List,
        metrics: Dict[str, str] = None,
        output_dir: str = '.',
        single_metric: str = None,
        output_file: str = 'profiling_stats.png'
):
    """Generate normalized bar plots of profiling statistics in a single PNG file with subplots.

    Args:
        profilers: List of profiler instances.
        metrics: Dict mapping profiler class names to metric keys (e.g., {'CPUProfiler': 'execution_time'}).
        output_dir: Directory to save the plot.
        single_metric: If specified, plot only this metric; otherwise, plot subplots for each metric.
        output_file: Name of the output PNG file (default: 'profiling_stats.png').
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Default metrics if not specified
    if metrics is None:
        metrics = {
            'CPUProfiler': 'execution_time',
            'DiskProfiler': 'write_bytes',
            'FunctionProfiler': 'call_count',
            'MemoryProfiler': 'peak_mb',
            'NetworkProfiler': 'bytes_sent'
        }

    # Collect all labels to align data
    all_labels = set()
    for profiler in profilers:
        for stat in profiler.get_stats():
            all_labels.add(stat['label'])
    all_labels = sorted(list(all_labels))  # Convert to list for indexing

    if not all_labels:
        print("No profiling data available to plot.")
        return

    # Simplify labels for clarity
    short_labels = [f"S{i + 1}" for i in range(len(all_labels))]  # S1, S2, S3, ...
    label_mapping = dict(zip(all_labels, short_labels))

    # Determine which metrics to plot
    metrics_to_plot = [single_metric] if single_metric else list(metrics.values())
    num_metrics = len(metrics_to_plot)

    if num_metrics == 0:
        print("No metrics to plot.")
        return

    # Calculate subplot grid: limit to 2 columns for readability
    cols = min(2, math.ceil(math.sqrt(num_metrics)))
    rows = math.ceil(num_metrics / cols)

    # Create a single figure with subplots
    fig, axes = plt.subplots(rows, cols, figsize=(12, rows * 4), constrained_layout=True)
    fig.suptitle('Profiling Statistics (Normalized)', fontsize=16)

    # Flatten axes array for easy iteration
    if num_metrics == 1:
        axes = [axes]
    else:
        axes = axes.flatten()

    for idx, metric in enumerate(metrics_to_plot):
        ax = axes[idx]
        values = []
        raw_values = []
        unit = ''

        # Collect data for the metric
        for label in all_labels:
            value = 0
            raw_value = 0
            for profiler in profilers:
                metric_key = metrics.get(profiler.__class__.__name__, 'unknown')
                if metric_key != metric:
                    continue
                stats = profiler.get_stats()
                label_metrics = {stat['label']: stat['metrics'] for stat in stats}
                metrics_data = label_metrics.get(label, {})
                raw_value = metrics_data.get(metric_key, 0)
                value = raw_value
                # Apply unit conversion
                if metric_key in ['write_bytes', 'bytes_sent']:
                    value /= 1024  # Convert bytes to KB
                    unit = 'KB'
                elif metric_key == 'execution_time':
                    unit = 'seconds'
                elif metric_key == 'peak_mb':
                    unit = 'MB'
                elif metric_key == 'call_count':
                    unit = 'counts'
                break  # Only one profiler per metric
            values.append(value)
            raw_values.append(raw_value)

        if not any(v != 0 for v in values):
            ax.set_visible(False)
            continue

        # Normalize values to 0-1
        max_value = max(values) if max(values) > 0 else 1
        normalized_values = [v / max_value for v in values]

        # Plot normalized bars
        x_positions = np.arange(len(all_labels))
        bars = ax.bar(x_positions, normalized_values, color='skyblue')

        # Add raw values as text on top of bars
        for bar, raw_value in zip(bars, raw_values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, height, f'{raw_value:.2f}',
                    ha='center', va='bottom', fontsize=8)

        ax.set_ylim(0, 1.1)  # Slightly above 1 to accommodate text
        ax.set_xticks(x_positions)
        ax.set_xticklabels([label_mapping[l] for l in all_labels], rotation=45, ha='right')
        ax.set_xlabel('Profiled Sections (S#)')
        ax.set_ylabel('Normalized Value (0-1)')
        ax.set_title(f'Metric: {metric} ({unit})')

    # Hide unused subplots
    for idx in range(num_metrics, len(axes)):
        axes[idx].set_visible(False)

    # Add a legend for section mapping
    section_legend = "\n".join([f"{short}: {orig}" for orig, short in label_mapping.items()])
    fig.text(0.95, 0.5, f"Section Mapping:\n{section_legend}", fontsize=10, verticalalignment='center')

    # Save the plot with the specified output file name
    output_path = os.path.join(output_dir, output_file)
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()
    print(f"Combined profiling plot saved to {os.path.abspath(output_path)}")
