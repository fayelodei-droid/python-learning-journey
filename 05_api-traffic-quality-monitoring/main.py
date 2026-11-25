"""Run the monitoring pipeline on sample HTTP traffic logs."""

from pathlib import Path
from pprint import pprint

from api_monitor import analyze_api_logs


def main():
    data_path = Path(__file__).resolve().parent / "data" / "api_logs.txt"
    logs = data_path.read_text(encoding="utf-8").splitlines()
    report = analyze_api_logs(logs)

    print("API Traffic Quality Report")
    print("=" * 28)
    pprint(report, sort_dicts=False)
    print(f"\nAverage response time: {report['average_response_time']:.2f} ms")


if __name__ == "__main__":
    main()
