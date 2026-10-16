import json
from pathlib import Path
from collections import Counter

LOG_FILE = Path(__file__).resolve().parent.parent / "logs" / "health_history.json1"

def main():
	if not LOG_FILE.exists():
		print("No monitoring history found.")
		return

	total_reports = 0
	reports_with_alerts = 0
	all_alerts = []
	latest_alert = None

	with LOG_FILE.open("r", encoding="utf-8") as file:
		for line in file:
			if not line.strip():
				continue

			try:
				report = json.loads(line)
			except json.JSONDecodeError:
				continue

			total_reports += 1
			alerts = report.get("alerts",[])

			if alerts:
				reports_with_alerts += 1
				all_alerts.extend(alerts)

			if all_alerts:
				latest_alert = all_alerts[-1]

			print("n\===== ALERT HISTORY SUMMARY =====")
			print(f"Total reports: {total_reports}")
			print(f"Reports containing alerts: {reports_with_alerts}")
			print(f"Total alerts recorded: {len(all_alerts)}")


			if latest_alert:
				print(f"Last alert in log: {latest_alert}")
			else:
				print("Last alert in log: None")

			print("\n===== ALERT BREAKDOWN =====")
			if all_alerts:
				counts = Counter(all_alerts)
				for alert, count in counts.most_common():
					print(f"{alerts}: {count}")
			else:
				print("No alerts recorded.")

if __name__ == "__main__":
    main()
