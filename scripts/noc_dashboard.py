import json
import time 
from pathlib import Path

LOG_FILE = Path(__file__).resolve().parent.parent / "log" / "health_history,json1"

def load_latest_report():
	if not LOG_FILE.exists():	
		return None

	with LOG_FILE.open("r", encoding="utf-8") as file:
		lines = file.readlines()

	if not lines:
		return None

	return json.loads(lines[-1])

def show_dashboard():
	report = load_latest_report()

	print("\n" + "=" * 44)
	print("       MINI SYSADMIN - NOC DASHBOARD")
	print("=" * 44)

	if report is None:
		print("NO MONITORING DATA FOUND.")
		print("Run: python scripts/health_check.py")
		return

	print(f"Hostname:     {report.get('hostname', 'Unknown')}")
	print(f"Operating system: {report.get('operating_system', 'Unknown')}")
	print("-" * 44)
	print(f"CPU usage:     {report.get('cpu_usage_percent', 'N/A')}%")
	print(f"Memory usage:  {report.get('memory_usage_percent', 'N/A')}%")
	print(f"Disk usage:    {report.get('disk_usage_percent', 'N/A')}%")
	print(f"Uptime:        {report.get('uptime_hours', 'N/A')} hours")
	print(f"Network:       {report.get('network_status', 'Unknown')}")
	print("-" * 44)

	alerts = report.get("alerts", [])

	if alerts:
		print("ALERTS:")
		for alert in alerts:
			print(f"  [!] {alert}")
		
	else:
		print("ALERTS: None recorded in latest report")

	print("=" * 44)
	print(f"Last updated: {report.get('timestamp_utc', 'Unknown')}")

if __name__ == "__main__":
	try:
		while True:
			show_dashboard()
			time.sleep(5)
	except KeyboardInterrupt:
			print("\nNOC dashboard stopped.")

