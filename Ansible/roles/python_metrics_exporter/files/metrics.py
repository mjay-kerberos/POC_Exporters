#!/usr/bin/python3
import csv
import os
import subprocess

def get_job_id_from_pid(pid):
    cmd = f"grep 'slurm' /proc/{pid}/cgroup | grep -o 'job_[0-9]*' | grep -o '[0-9]*'"
    try:
        job_id = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
        return int(job_id.split('\n')[0])  # taking the first one assuming they're the same
    except subprocess.CalledProcessError:
        return None

def parse_csv(file_path):
    data = []
    try:
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cleaned_row = {k.strip(): v.strip() for k, v in row.items()}
                data.append(cleaned_row)
    except Exception as e:
        print(f"Error parsing CSV file {file_path}: {e}")
    return data

def get_gpu_count_per_job():
    gpu_map = {}
    try:
        squeue_output = subprocess.check_output("squeue -o '%.18i %.10b'", shell=True).decode('utf-8').splitlines()
        for line in squeue_output[1:]:  # Skip header
            parts = line.strip().split()
            if len(parts) >= 2:
                jobid, gpu_field = parts[0], parts[1]
                if 'gpu:' in gpu_field:
                    gpu_count = gpu_field.split(':')[-1]
                else:
                    gpu_count = '0'
                gpu_map[jobid] = gpu_count
    except subprocess.CalledProcessError as e:
        print(f"Error getting GPU count via squeue: {e}")
    return gpu_map


# Run nvidia-smi and gather GPU/app data
try:
    subprocess.run('nvidia-smi --query-gpu=gpu_uuid,index,name,utilization.gpu --format=csv > gpu_info.csv', shell=True, check=True)
    subprocess.run('nvidia-smi --query-compute-apps=pid,used_gpu_memory,gpu_uuid --format=csv > compute_apps_usage.csv', shell=True, check=True)
except subprocess.CalledProcessError as e:
    print(f"Error running nvidia-smi commands: {e}")
    exit(1)

gpu_info = parse_csv('gpu_info.csv')
compute_apps_usage = parse_csv('compute_apps_usage.csv')
job_gpu_count_map = get_gpu_count_per_job()

# Prepare the mapping
mapping = {}
for app in compute_apps_usage:
    uuid = app.get('gpu_uuid', '')
    for gpu in gpu_info:
        if gpu.get('uuid', '') == uuid:
            index = gpu.get('index', '')
            pid = app.get('pid', '')
            used_mem = app.get('used_gpu_memory [MiB]', '0').strip(' MiB') or '0'
            utilization = gpu.get('utilization.gpu [%]', '0').strip(' %') or '0'
            mapping[index] = {
                'uuid': uuid,
                'pid': pid,
                'utilization': utilization,
                'used_memory_mib': used_mem
            }

# Write Prometheus metrics
output_file = "/var/lib/node_exporter/textfile_collector/gpu_metrics.prom"
os.makedirs(os.path.dirname(output_file), exist_ok=True)

with open(output_file, 'w') as f:
    for key, value in mapping.items():
        minor_number = key
        gpu_utilization = value['utilization']
        gpu_memory_usage_bytes = int(value['used_memory_mib']) * 1024 * 1024
        job_id = get_job_id_from_pid(value['pid'])

        if job_id:
            job_id_str = str(job_id)
            gpu_count = job_gpu_count_map.get(job_id_str, "0")

            f.write(f'cgroups_nvidia_gpu_utilization{{gpu_id="{minor_number}", job_id="{job_id}", job_gpu_count="{gpu_count}"}} {gpu_utilization}\n')
            f.write(f'cgroups_nvidia_gpu_memory_usage_in_bytes{{gpu_id="{minor_number}", job_id="{job_id}", job_gpu_count="{gpu_count}"}} {gpu_memory_usage_bytes}\n')
