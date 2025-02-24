# NVIDIA GPU Exporter (Python)

This script collects GPU and I/O metrics from an NVIDIA GPU and outputs them in a format compatible with Prometheus node exporter.

## Requirements

- Python 3.x
- NVIDIA GPU with `nvidia-smi` tool

## Usage

```sh
python3 nvidia_gpu_exporter.py
```

## Metrics Collected

- `cgroups_nvidia_gpu_utilization`: GPU utilization percentage.
- `cgroups_nvidia_gpu_memory_usage_bytes`: GPU memory usage in bytes.
- `cgroups_io_read_bytes`: I/O read bytes.
- `cgroups_io_write_bytes`: I/O write bytes.
```