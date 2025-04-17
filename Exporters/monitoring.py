import os
import time
import sqlite3
import subprocess
from datetime import datetime, timedelta
from threading import Thread
from prometheus_client import start_http_server, Gauge, REGISTRY

# ========== DATABASE SETUP ==========
conn = sqlite3.connect('utilization.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS gpu_utilization_raw (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    account TEXT,
    utilization_percent REAL
)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS gpu_utilization_aggregate (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE,
    period TEXT,
    account TEXT,
    average_utilization REAL
)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS storage_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE DEFAULT CURRENT_DATE,
    usage_gb REAL
    usage_percent REAL
)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS cpu_utilization (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    period TEXT,
    account TEXT,
    cpu_hours REAL,
    gpu_hours REAL
)""")

conn.commit()

# ========== PROMETHEUS METRICS ==========
gpu_weekly_metric = Gauge("weekly_gpu_utilization", "Weekly average GPU utilization", ["account"])
gpu_monthly_metric = Gauge("monthly_gpu_utilization", "Monthly average GPU utilization", ["account"])
cpu_weekly_metric = Gauge("weekly_cpu_usage_hours", "Weekly CPU usage", ["account"])
cpu_monthly_metric = Gauge("monthly_cpu_usage_hours", "Monthly CPU usage", ["account"])
storage_monthly_metric = Gauge("monthly_storage_usage_gb", "Monthly average DDN storage used")
storage_used_percent_metric = Gauge("monthly_storage_usage_percent", "Monthly average DDN storage percent used")

# ========== GPU UTILIZATION ==========
gpu_enabled = True  # Global flag to disable if nvidia-smi is not present
def check_nvidia_smi_available():
    global gpu_enabled
    try:
        subprocess.check_output("nvidia-smi -L", shell=True, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("[WARN] `nvidia-smi` not available on this node. Skipping GPU collection.")
        gpu_enabled = False
    except FileNotFoundError:
        print("[WARN] `nvidia-smi` command not found. Skipping GPU collection.")
        gpu_enabled = False

def collect_gpu_utilization():
    if not gpu_enabled:
        return

    while True:
        try:
            result = subprocess.check_output(
                "nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits",
                shell=True
            ).decode().strip().splitlines()

            timestamp = datetime.now()
            for idx, util in enumerate(result):
                account = f"gpu{idx}"
                cursor.execute(
                    "INSERT INTO gpu_utilization_raw (timestamp, account, utilization_percent) VALUES (?, ?, ?)",
                    (timestamp, account, float(util))
                )
            conn.commit()
        except subprocess.CalledProcessError:
            print("[WARN] Error executing nvidia-smi — skipping this cycle.")
        except Exception as e:
            print(f"[ERROR] GPU collection failed: {e}")
        time.sleep(30)


def aggregate_daily_gpu():
    yesterday = (datetime.now() - timedelta(days=1)).date()
    cursor.execute("""
        INSERT INTO gpu_utilization_aggregate (date, period, account, average_utilization)
        SELECT DATE(timestamp), 'day', account, AVG(utilization_percent)
        FROM gpu_utilization_raw
        WHERE DATE(timestamp) = ?
        GROUP BY account
    """, (yesterday,))
    conn.commit()

def aggregate_weekly_gpu():
    cursor.execute("""
        INSERT INTO gpu_utilization_aggregate (date, period, account, average_utilization)
        SELECT DATE('now'), 'week', account, AVG(average_utilization)
        FROM gpu_utilization_aggregate
        WHERE period = 'day' AND date >= DATE('now', '-7 day')
        GROUP BY account
    """)
    conn.commit()

def aggregate_monthly_gpu():
    cursor.execute("""
        INSERT INTO gpu_utilization_aggregate (date, period, account, average_utilization)
        SELECT DATE('now'), 'month', account, AVG(average_utilization)
        FROM gpu_utilization_aggregate
        WHERE period = 'week' AND date >= DATE('now', '-30 day')
        GROUP BY account
    """)
    conn.commit()

# ========== CPU UTILIZATION ==========
def collect_cpu_utilization(period):
    try:
        cmd = f"sreport cluster AccountUtilizationByUser start=-{period} format=Account,CPU_Hours,GPU_Hours"
        output = subprocess.check_output(cmd, shell=True).decode().strip().splitlines()

        for line in output[1:]:
            parts = line.split()
            if len(parts) < 3:
                continue
            account, cpu_hours, gpu_hours = parts[0], float(parts[1]), float(parts[2])
            cursor.execute("""
                INSERT INTO cpu_utilization (period, account, cpu_hours, gpu_hours)
                VALUES (?, ?, ?, ?)
            """, (period, account, cpu_hours, gpu_hours))
        conn.commit()
    except Exception as e:
        print(f"[ERROR] CPU collection failed ({period}): {e}")

# ========== STORAGE UTILIZATION ==========
def collect_storage_usage():
    try:
        output = subprocess.check_output("df -h /rs01", shell=True).decode().strip().splitlines()
        if len(output) < 2:
            return
        parts = output[1].split()
        used = parts[2]        # Column: Used Size (e.g., 179T)
        used_percent = parts[4]  # Column: Used % (e.g., 17%)

        # Convert storage units
        if used.endswith("G"):
            usage_gb = float(used[:-1])
        elif used.endswith("T"):
            usage_gb = float(used[:-1]) * 1024
        elif used.endswith("P"):
            usage_gb = float(used[:-1]) * 1024 * 1024
        else:
            usage_gb = 0

        # Convert percentage string to float
        used_percent_value = float(used_percent.strip('%'))

        cursor.execute("INSERT INTO storage_usage (usage_gb, used_percent) VALUES (?, ?)", (usage_gb, used_percent_value))
        conn.commit()

    except Exception as e:
        print(f"[ERROR] Storage collection failed: {e}")


def aggregate_monthly_storage():
    cursor.execute("""
        SELECT AVG(usage_gb), AVG(used_percent) FROM storage_usage
        WHERE date >= DATE('now', '-30 day')
    """)
    avg_gb, avg_percent = cursor.fetchone()
    storage_monthly_metric.set(avg_gb)
    storage_used_percent_metric.set(avg_percent or 0)

# ========== PROMETHEUS UPDATE ==========
def update_prometheus_metrics():
    # GPU weekly
    cursor.execute("SELECT account, average_utilization FROM gpu_utilization_aggregate WHERE period = 'week'")
    for account, avg in cursor.fetchall():
        gpu_weekly_metric.labels(account=account).set(avg)

    # GPU monthly
    cursor.execute("SELECT account, average_utilization FROM gpu_utilization_aggregate WHERE period = 'month'")
    for account, avg in cursor.fetchall():
        gpu_monthly_metric.labels(account=account).set(avg)

    # CPU weekly
    cursor.execute("SELECT account, cpu_hours FROM cpu_utilization WHERE period = '7days'")
    for account, hours in cursor.fetchall():
        cpu_weekly_metric.labels(account=account).set(hours)

    # CPU monthly
    cursor.execute("SELECT account, cpu_hours FROM cpu_utilization WHERE period = '30days'")
    for account, hours in cursor.fetchall():
        cpu_monthly_metric.labels(account=account).set(hours)

    aggregate_monthly_storage()

# ========== SCHEDULING ==========
def schedule_task(interval_seconds, func):
    def loop():
        while True:
            func()
            time.sleep(interval_seconds)
    Thread(target=loop, daemon=True).start()

# ========== MAIN ==========
if __name__ == "__main__":
    # Start Prometheus endpoint
    start_http_server(9060)

    # Check if GPU metrics can be collected
    check_nvidia_smi_available()

    # GPU data collection (only if enabled)
    if gpu_enabled:
        Thread(target=collect_gpu_utilization, daemon=True).start()

    # Daily tasks
    schedule_task(86400, aggregate_daily_gpu)
    schedule_task(86400, collect_storage_usage)
    schedule_task(86400, lambda: collect_cpu_utilization("7days"))
    schedule_task(2592000, lambda: collect_cpu_utilization("30days"))  # monthly
    schedule_task(604800, aggregate_weekly_gpu)  # weekly
    schedule_task(2592000, aggregate_monthly_gpu)  # monthly

    # Update metrics every 5 minutes
    schedule_task(300, update_prometheus_metrics)

    print(" Monitoring service started on port 9060...")
    while True:
        time.sleep(3600)
