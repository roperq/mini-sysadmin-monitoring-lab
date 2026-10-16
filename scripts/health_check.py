import json
import platform
import socket
import shutil
import time
from datetime import datetime, timezone
from pathlib import Path
import psutil

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

PROJECT_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

uptime_seconds = int(time.time() - psutil.boot_time())

memory = psutil.virtual_memory()
disk = shutil.disk_usage("/")
cpu_percent = psutil.cpu_percent(interval=1)
CPU_WARNING = 80
MEMORY_WARNING = 85
DISK_WARNING = 85

alerts = []

try:
	with socket.create_connection(("example.com", 443), timeout=3):
		network_status = "ONLINE"
except OSError:
		network_status = "OFFLINE"
if network_status == "OFFLINE":
		alerts.append(f"[{timestamp()}] CRITICAL: Network connectivity check failed")

if cpu_percent >= CPU_WARNING:
	alerts.append(f"[{timestamp()}] WARNING: High CPU usage")

if memory.percent >= MEMORY_WARNING:
	alrets.append(f"[{timestamp()}] WARNING: High Memory Usage")

disk_percent = disk.used / disk.total * 100

if disk_percent >= DISK_WARNING:
	alerts.append(f"[{timestamp()}] WARNING: Low disk space")

report = {
"timestamp_utc": datetime.now(timezone.utc).isoformat(),
"hostname": platform.node(),
"operating_system": platform.platform(),
"cpu_usage_percent": cpu_percent,
"network_status": network_status,
"memory_usage_percent": memory.percent,
"memory_available_mb": round(memory.available / (1024 ** 2), 2),
"disk_usage_percent": round(disk.used / disk.total * 100, 2),
"disk_free_gb": round(disk.free / (1024 ** 3), 2),
"uptime_hours": round(uptime_seconds /3600, 2),
"alerts": alerts,
}

print("\n===== MINI SYSADMIN HEALTH CHECK =====")
for metric,  value in report.items():
	print(f"{metric}: {value}")

print("Alerts:", alerts if alerts else "None - system within thresholds")

log_file = LOG_DIR / "health_history.json1"

with log_file.open("a", encoding="utf-8") as file:
	file.write(json.dumps(report) + "\n")

print(f"\nReport saved to: {log_file}")

