#!/usr/bin/python3
import subprocess
import os
import time
import datetime

PROMETHEUS_FILE = "/var/lib/node_exporter/textfile_collector/cpu_usage_report.prom"

def run_command(cmd):
    """Runs a shell command and returns the output."""
    try:
        result = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {cmd}\n{e}")
        return ""

def get_weekly_cpu_utilization():
    """Fetches CPU utilization for the past 7 days using `sreport`."""
    today = datetime.date.today()
    seven_days_ago = today - datetime.timedelta(days=7)

    cmd = f"""sreport cluster Utilization start={seven_days_ago.strftime('%Y-%m-%d')} end={today.strftime('%Y-%m-%d')} | awk '/slurm/ {{print $2}}'"""
    output = run_command(cmd)

    try:
        return float(output)  # Convert CPU minutes to float
    except ValueError:
        return 0

def get_monthly_cpu_utilization():
    """Fetches CPU utilization for the last full month using `sreport`."""
    today = datetime.date.today()
    first_day_of_month = today.replace(day=1)
    last_day_of_month = (first_day_of_month.replace(day=28) + datetime.timedelta(days=4)).replace(day=1) - datetime.timedelta(days=1)

    cmd = f"""sreport cluster Utilization start={first_day_of_month.strftime('%Y-%m-%d')} end={last_day_of_month.strftime('%Y-%m-%d')} | awk '/slurm/ {{print $2}}'"""
    output = run_command(cmd)

    try:
        return float(output)  # Convert CPU minutes to float
    except ValueError:
        return 0

def write_to_prometheus(cpu_weekly, cpu_monthly):
    """Writes CPU utilization data to a Prometheus file."""
    timestamp = int(time.time())

    metrics = f"""# HELP slurm_cpus_avg_weekly Average CPU usage (minutes) over the past week
# TYPE slurm_cpus_avg_weekly gauge
slurm_cpus_avg_weekly {cpu_weekly} {timestamp}

# HELP slurm_cpus_avg_monthly Average CPU usage (minutes) over the past month
# TYPE slurm_cpus_avg_monthly gauge
slurm_cpus_avg_monthly {cpu_monthly} {timestamp}
"""

    with open(PROMETHEUS_FILE, "w") as f:
        f.write(metrics)
    print(f"Metrics written to {PROMETHEUS_FILE}")

def main():
    """Main function to calculate and save CPU utilization metrics."""
    today = datetime.date.today()
    last_day_of_month = (today.replace(day=28) + datetime.timedelta(days=4)).replace(day=1) - datetime.timedelta(days=1)

    if today == last_day_of_month:  # If today is the last day of the month
        cpu_monthly = get_monthly_cpu_utilization()
    else:
        cpu_monthly = 0

    cpu_weekly = get_weekly_cpu_utilization()

    write_to_prometheus(cpu_weekly, cpu_monthly)

if __name__ == "__main__":
    main()
