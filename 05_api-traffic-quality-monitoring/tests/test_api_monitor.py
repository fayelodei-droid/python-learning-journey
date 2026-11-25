"""Automated tests for API traffic quality monitoring."""

import unittest

from api_monitor import analyze_api_logs, parse_log, validate_log


SAMPLE_LOGS = [
    "GET /api/users 200 120",
    "POST /api/orders 201 350",
    "GET /api/products 200 180",
    "DELETE /api/users/42 500 900",
    "GET /api/stats 200 250",
    "PATCH /api/users/42 503 1200",
    "GET /api/search 200 160",
    "INVALID_LOG",
    "POST /api/orders 201",
    "GET /api/users abc 100",
    "GET /api/users 200 -50",
    "GET /wrong/path 200 100",
]


class ValidateLogTests(unittest.TestCase):
    def test_valid_log(self):
        self.assertTrue(validate_log("GET /api/users 200 120"))

    def test_inclusive_status_boundaries_and_zero_time(self):
        self.assertTrue(validate_log("GET /api/users 100 0"))
        self.assertTrue(validate_log("GET /api/users 599 10"))

    def test_invalid_status_values(self):
        self.assertFalse(validate_log("GET /api/users 99 10"))
        self.assertFalse(validate_log("GET /api/users 600 10"))
        self.assertFalse(validate_log("GET /api/users abc 10"))

    def test_invalid_response_time(self):
        self.assertFalse(validate_log("GET /api/users 200 -50"))
        self.assertFalse(validate_log("GET /api/users 200 abc"))

    def test_invalid_method_endpoint_and_structure(self):
        self.assertFalse(validate_log("HEAD /api/users 200 100"))
        self.assertFalse(validate_log("GET /wrong/path 200 100"))
        self.assertFalse(validate_log("INVALID_LOG"))
        self.assertFalse(validate_log("POST /api/orders 201"))
        self.assertFalse(validate_log(""))
        self.assertFalse(validate_log("  "))

    def test_allowed_methods(self):
        for method in ("GET", "POST", "PUT", "DELETE", "PATCH"):
            with self.subTest(method=method):
                self.assertTrue(validate_log(f"{method} /api/users 200 10"))


class ParseLogTests(unittest.TestCase):
    def test_typed_dictionary(self):
        result = parse_log("GET /api/users 200 120")
        self.assertEqual(result, {
            "method": "GET", "endpoint": "/api/users", "status": 200,
            "response_time": 120,
        })
        self.assertIsInstance(result["status"], int)
        self.assertIsInstance(result["response_time"], int)

    def test_original_string_is_unchanged(self):
        original = "GET /api/users 200 120"
        parse_log(original)
        self.assertEqual(original, "GET /api/users 200 120")


class AnalyzeApiLogsTests(unittest.TestCase):
    def test_summary_counts(self):
        report = analyze_api_logs(SAMPLE_LOGS)
        self.assertEqual(report["total_requests"], 7)
        self.assertEqual(report["total_invalid"], 5)
        self.assertEqual(report["server_errors"], 2)

    def test_average_response_time(self):
        report = analyze_api_logs(SAMPLE_LOGS)
        self.assertEqual(round(report["average_response_time"], 2), 451.43)

    def test_invalid_logs_original_and_ordered(self):
        report = analyze_api_logs(SAMPLE_LOGS)
        self.assertEqual(report["invalid_logs"], SAMPLE_LOGS[7:])

    def test_valid_logs_order_and_structure(self):
        report = analyze_api_logs(SAMPLE_LOGS)
        self.assertEqual(
            [entry["method"] for entry in report["valid_logs"]],
            ["GET", "POST", "GET", "DELETE", "GET", "PATCH", "GET"],
        )
        self.assertEqual(report["valid_logs"][0], {
            "method": "GET", "endpoint": "/api/users", "status": 200,
            "response_time": 120,
        })

    def test_empty_input(self):
        self.assertEqual(analyze_api_logs([]), {
            "valid_logs": [], "invalid_logs": [], "total_requests": 0,
            "total_invalid": 0, "server_errors": 0,
            "average_response_time": 0,
        })

    def test_input_immutability(self):
        logs = SAMPLE_LOGS.copy()
        before = logs.copy()
        analyze_api_logs(logs)
        self.assertEqual(logs, before)

    def test_all_invalid_input(self):
        report = analyze_api_logs(["BAD", "", "GET /outside 200 50"])
        self.assertEqual(report["total_requests"], 0)
        self.assertEqual(report["total_invalid"], 3)
        self.assertEqual(report["average_response_time"], 0)


if __name__ == "__main__":
    unittest.main()
