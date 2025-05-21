### POC Exporters README (`README.md`)


# GPU and I/O Exporters

This repository Contains proof-of-concept exporters written in Python and Go for collecting GPU and I/O metrics. These exporters are designed to work with Prometheus for monitoring system performance.

## Exporters

- `nvidia_gpu_exporter.py`: A Python script that collects GPU utilization, memory usage, and I/O metrics.
- `gpu_io_exporter.go`: A Go script that collects GPU utilization, memory usage, and I/O metrics.

## Requirements

- Python 3.x
- Go 1.16+
- Prometheus
- NVIDIA GPU with `nvidia-smi` tool

## Usage

### Python Script

```sh
python3 nvidia_gpu_exporter.py
```

### Go Script

```sh
go run gpu_io_exporter.go
```


## Metrics Collected

- GPU Utilization
- GPU Memory Usage
- I/O Read Bytes
- I/O Write Bytes
