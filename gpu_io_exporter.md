# GPU and I/O Exporter (Go)

This Go script collects GPU and I/O metrics and exposes them for Prometheus.

## Requirements

- Go 1.16+
- NVIDIA GPU with `nvidia-smi` tool

## Usage

```sh
go run gpu_io_exporter.go
```

## Metrics Collected

- `gpu_utilization`: GPU utilization percentage.
- `gpu_memory_usage_bytes`: GPU memory usage in bytes.
- `io_read_bytes`: I/O read bytes.
- `io_write_bytes`: I/O write bytes.
```