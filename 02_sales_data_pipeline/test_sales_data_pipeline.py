"""Integration tests for the pipeline using temporary CSV files."""
import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("sales_data_pipeline.py")


class TestSalesPipeline(unittest.TestCase):
    def run_pipeline(self, rows, headers=("product", "price", "quantity")):
        with tempfile.TemporaryDirectory() as folder:
            directory = Path(folder)
            with (directory / "sales.csv").open("w", encoding="utf-8", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=headers)
                writer.writeheader()
                writer.writerows(rows)
            completed = subprocess.run(
                [sys.executable, str(SCRIPT)], cwd=directory,
                capture_output=True, text=True, check=False
            )
            result_path = directory / "sales_report.json"
            report = json.loads(result_path.read_text(encoding="utf-8")) if result_path.exists() else None
            return completed, report

    def test_totals_and_unique_products(self):
        process, report = self.run_pipeline([
            {"product": "Laptop", "price": "100", "quantity": "2"},
            {"product": "Mouse", "price": "10", "quantity": "3"},
            {"product": "Laptop", "price": "100", "quantity": "1"},
        ])
        self.assertEqual(process.returncode, 0)
        self.assertEqual(report["total_revenue"], 330.0)
        self.assertEqual(report["average_revenue"], 110.0)
        self.assertEqual(report["unique_products"], 2)

    def test_invalid_and_nonfinite_rows_are_skipped(self):
        process, report = self.run_pipeline([
            {"product": "A", "price": "50", "quantity": "2"},
            {"product": "B", "price": "nan", "quantity": "1"},
            {"product": "C", "price": "inf", "quantity": "1"},
            {"product": "D", "price": "-1", "quantity": "2"},
            {"product": "E", "price": "oops", "quantity": "1"},
            {"product": " ", "price": "20", "quantity": "1"},
            {"product": "F", "price": "5", "quantity": "0"},
        ])
        self.assertEqual(process.returncode, 0)
        self.assertEqual(report["total_revenue"], 100.0)
        self.assertEqual(report["average_revenue"], 100.0)
        self.assertEqual(report["unique_products"], 1)

    def test_all_invalid_rows_produce_zero_metrics(self):
        process, report = self.run_pipeline([
            {"product": "A", "price": "0", "quantity": "1"},
            {"product": "B", "price": "bad", "quantity": "1"},
        ])
        self.assertEqual(process.returncode, 0)
        self.assertEqual(report, {"total_revenue": 0, "average_revenue": 0, "unique_products": 0})

    def test_missing_headers_raises_clear_error(self):
        process, report = self.run_pipeline([{"product": "A", "price": "5"}], ("product", "price"))
        self.assertNotEqual(process.returncode, 0)
        self.assertIn("CSV must include", process.stderr)
        self.assertIsNone(report)


if __name__ == "__main__":
    unittest.main()
