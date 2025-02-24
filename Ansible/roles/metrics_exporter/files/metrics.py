#!/usr/bin/python3
"""
Metrics Collection Script

This script collects GPU and I/O metrics from the system and exports them
in a format compatible with Prometheus node exporter's textfile collector.
It maps process metrics to SLURM job IDs when available.
"""

import csv
import subprocess
import os
import tempfile
import logging
import logging.handlers
import argparse
import sys
from contextlib import contextmanager

def setup_logging(log_to_file=False, debug=False):
    """
    Configure logging with options for file output or systemd-compatible logging.
    
    :param log_to_file: Whether to log to a file.
    :param debug: Whether to enable debug logging.
    """
    logger = logging.getLogger()
    
    # Clear any existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Set log level
    log_level = logging.DEBUG if debug else logging.INFO
    logger.setLevel(log_level)
    
    # Format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    if log_to_file:
        # Ensure log directory exists
        log_dir = os.path.dirname('/var/log/job_metrics')
        if not os.path.exists(log_dir):
            try:
                os.makedirs(log_dir)
            except OSError as e:
                print(f"Error creating log directory: {e}", file=sys.stderr)
                # Fall back to stderr logging if we can't create the log directory
                log_to_file = False
    
    if log_to_file:
        # Set up file handler with rotation
        file_handler = logging.handlers.RotatingFileHandler(
            '/var/log/job_metrics/metrics.log',
            maxBytes=10485760,  # 10MB
            backupCount=5
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    else:
        # For systemd, log to stderr which will be captured by journald
        stream_handler = logging.StreamHandler(sys.stderr)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
    
    return logger


def parse_arguments():
    """
    Parse command-line arguments.

    :return: Parsed arguments object.
    """
    parser = argparse.ArgumentParser(
        description='Collect and export GPU and I/O metrics to Prometheus'
    )
    parser.add_argument(
        '--output',
        default='/var/lib/node_exporter/textfile_collector/metrics.prom',
        help='Path to output metrics file'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug logging'
    )
    parser.add_argument(
        '--log-to-file',
        action='store_true',
        help='Log to file instead of stderr (for systemd)'
    )
    return parser.parse_args()


@contextmanager
def temp_csv_file():
    """
    Context manager for creating and cleaning up temporary CSV files.

    :yield: Path to the temporary file.
    """
    temp_file = tempfile.NamedTemporaryFile(
        mode='w+',
        suffix='.csv',
        delete=False
    )
    try:
        temp_file.close()
        yield temp_file.name
    finally:
        try:
            os.unlink(temp_file.name)
        except OSError as e:
            logging.warning(f"Failed to delete temporary file {temp_file.name}: {e}")


def get_job_id_from_pid(pid):
    """
    Extracts the SLURM job ID for a given process ID (PID) from the cgroup info.

    :param pid: Process ID for which to find the job ID.
    :return: Job ID as an integer if found, None otherwise.
    """
    if not pid.isdigit():
        logging.debug(f"Invalid PID format: {pid}")
        return None
    
    try:
        cgroup_path = f"/proc/{pid}/cgroup"
        if not os.path.exists(cgroup_path):
            return None
            
        with open(cgroup_path, 'r') as f:
            for line in f:
                if 'slurm' in line and 'job_' in line:
                    # Extract job ID using string operations
                    parts = line.split('job_')
                    if len(parts) > 1:
                        job_part = parts[1].split('/')[0]
                        if job_part.isdigit():
                            return int(job_part)
    except (IOError, IndexError) as e:
        logging.debug(f"Error reading cgroup for PID {pid}: {e}")
    
    return None


def parse_csv(file_path):
    """
    Parses a CSV file into a list of dictionaries.

    :param file_path: Path to the CSV file to parse.
    :return: A list of dictionaries, each representing a row in the CSV.
    """
    data = []
    try:
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cleaned_row = {k.strip(): v.strip() for k, v in row.items() if k is not None}
                data.append(cleaned_row)
    except IOError as e:
        logging.error(f"Failed to parse CSV file {file_path}: {e}")
        return []
    
    return data


def get_nvidia_metrics():
    """
    Gathers NVIDIA GPU metrics using the nvidia-smi tool.

    :return: A mapping dictionary containing GPU metrics keyed by GPU index.
    """
    gpu_metrics = {}

    with temp_csv_file() as gpu_info_path, temp_csv_file() as compute_apps_path:
        # Execute nvidia-smi commands to gather GPU info and compute application usage
        try:
            cmd_gpu_info = f"nvidia-smi --query-gpu=gpu_uuid,index,name,utilization.gpu --format=csv > {gpu_info_path}"
            cmd_apps_usage = f"nvidia-smi --query-compute-apps=pid,used_gpu_memory,gpu_uuid --format=csv > {compute_apps_path}"
            
            subprocess.run(cmd_gpu_info, shell=True, check=True)
            subprocess.run(cmd_apps_usage, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            logging.error(f"Error running nvidia-smi commands: {e}")
            return {}

        # Parse the output CSV files
        gpu_info = parse_csv(gpu_info_path)
        compute_apps_usage = parse_csv(compute_apps_path)

        # Prepare the mapping - each GPU can have multiple processes
        for gpu in gpu_info:
            if 'index' not in gpu or 'uuid' not in gpu:
                continue
                
            index = gpu['index']
            uuid = gpu['uuid']
            
            gpu_metrics[index] = {
                'uuid': uuid,
                'name': gpu.get('name', 'Unknown'),
                'utilization': gpu.get('utilization.gpu [%]', '0').strip(' %'),
                'processes': []
            }

        # Associate processes with GPUs
        for app in compute_apps_usage:
            if 'gpu_uuid' not in app or 'pid' not in app:
                continue
                
            uuid = app['gpu_uuid']
            
            # Find the GPU index for this UUID
            for index, gpu_data in gpu_metrics.items():
                if gpu_data['uuid'] == uuid:
                    gpu_data['processes'].append({
                        'pid': app['pid'],
                        'used_memory_mib': app.get('used_gpu_memory [MiB]', '0').strip(' MiB')
                    })

    return gpu_metrics


def get_io_metrics(pid_to_job):
    """
    Retrieves I/O metrics for a set of processes from the Linux proc filesystem.

    :param pid_to_job: A dictionary mapping PIDs to job IDs.
    :return: A dictionary where each key is a PID and each value is another dictionary 
             containing 'read_bytes' and 'write_bytes'.
    """
    io_metrics = {}
    
    for pid in pid_to_job:
        if pid_to_job[pid] is None:  # Skip if no job ID
            continue
            
        io_path = f'/proc/{pid}/io'
        if not os.path.exists(io_path):
            continue
            
        try:
            with open(io_path, 'r') as file:
                io_data = file.read()
            io_metrics[pid] = parse_io_data(io_data)
        except IOError as e:
            logging.debug(f"Error reading IO data for PID {pid}: {e}")
            continue
            
    return io_metrics


def parse_io_data(io_data):
    """
    Parses the content of an I/O metric file from the Linux proc filesystem.

    :param io_data: The content of an I/O metric file as a string.
    :return: A dictionary containing the I/O metrics.
    """
    io_info = {
        'read_bytes': 'N/A',
        'write_bytes': 'N/A'
    }
    
    for line in io_data.split('\n'):
        parts = line.split(':')
        if len(parts) == 2:
            key, value = parts
            key = key.strip()
            value = value.strip()
            
            if key == 'read_bytes' or key == 'write_bytes':
                io_info[key] = value
                
    return io_info


def write_to_textfile_collector(pid_to_job, gpu_metrics, io_metrics, output_path):
    """
    Writes GPU and I/O metrics to an output file formatted for Prometheus node exporter.

    :param pid_to_job: A dictionary mapping PIDs to job IDs.
    :param gpu_metrics: A dictionary containing GPU metrics for each GPU index.
    :param io_metrics: A dictionary containing I/O metrics for each PID.
    :param output_path: Path to output metrics file.
    """
    try:
        # Create directory if it doesn't exist
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        with open(output_path, 'w') as f:
            # Write GPU metrics
            for gpu_id, gpu_data in gpu_metrics.items():
                # Write GPU utilization
                f.write(f'nvidia_gpu_utilization{{gpu_id="{gpu_id}", gpu_name="{gpu_data["name"]}"}} {gpu_data["utilization"]}\n')
                
                # Write per-process GPU metrics
                for process in gpu_data['processes']:
                    pid = process['pid']
                    job_id = pid_to_job.get(pid)
                    
                    if job_id:
                        gpu_memory_usage_bytes = int(process['used_memory_mib']) * 1024 * 1024
                        f.write(f'cgroups_nvidia_gpu_utilization{{gpu_id="{gpu_id}", job_id="{job_id}", pid="{pid}"}} {gpu_data["utilization"]}\n')
                        f.write(f'cgroups_nvidia_gpu_memory_usage_bytes{{gpu_id="{gpu_id}", job_id="{job_id}", pid="{pid}"}} {gpu_memory_usage_bytes}\n')

            # Write I/O metrics
            for pid, metrics in io_metrics.items():
                job_id = pid_to_job.get(pid)
                
                if job_id and metrics['read_bytes'] != 'N/A' and metrics['write_bytes'] != 'N/A':
                    f.write(f'cgroups_io_read_bytes{{pid="{pid}", job_id="{job_id}"}} {metrics["read_bytes"]}\n')
                    f.write(f'cgroups_io_write_bytes{{pid="{pid}", job_id="{job_id}"}} {metrics["write_bytes"]}\n')
                    
        logging.info(f"Metrics successfully written to {output_path}")
        
    except IOError as e:
        logging.error(f"Failed to write metrics to {output_path}: {e}")


def main():
    """
    Main function that coordinates the metrics collection and export.
    """
    # Parse arguments
    args = parse_arguments()
    
    # Set up logging
    setup_logging(args.log_to_file, args.debug)
    
    logging.info("Starting metrics collection")
    
    # Create a mapping of PIDs to job IDs
    pid_to_job = {}
    for pid in os.listdir('/proc'):
        if pid.isdigit():
            job_id = get_job_id_from_pid(pid)
            if job_id:
                pid_to_job[pid] = job_id
    
    logging.debug(f"Found {len(pid_to_job)} processes with job IDs")
    
    # Collect GPU metrics
    gpu_metrics = get_nvidia_metrics()
    logging.debug(f"Collected metrics for {len(gpu_metrics)} GPUs")
    
    # Collect I/O metrics
    io_metrics = get_io_metrics(pid_to_job)
    logging.debug(f"Collected I/O metrics for {len(io_metrics)} processes")
    
    # Write to Prometheus-compatible output file
    write_to_textfile_collector(pid_to_job, gpu_metrics, io_metrics, args.output)
    
    logging.info("Metrics collection completed")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.exception(f"Unhandled exception: {e}")
        exit(1)