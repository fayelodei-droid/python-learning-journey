"""Unit tests for the original summary logic plus added validation."""
import unittest
from summarize_data import summarize_data


class TestSummarizeData(unittest.TestCase):
    def test_mean_default(self):
        self.assertEqual(summarize_data(10, 20, 30), 20)

    def test_sum(self):
        self.assertEqual(summarize_data(10, 20, 30, metric="sum"), 60)

    def test_rounding(self):
        self.assertEqual(summarize_data(1, 2, round_digits=1), 1.5)

    def test_empty_values(self):
        self.assertIsNone(summarize_data())

    def test_unsupported_metric(self):
        with self.assertRaises(ValueError):
            summarize_data(10, 20, metric="median")

    def test_string_value(self):
        with self.assertRaises(ValueError):
            summarize_data(10, "20")

    def test_infinite_value(self):
        with self.assertRaises(ValueError):
            summarize_data(10, float("inf"))

    def test_nan_value(self):
        with self.assertRaises(ValueError):
            summarize_data(float("nan"), 20)

    def test_invalid_precision(self):
        with self.assertRaises(ValueError):
            summarize_data(10, 20, round_digits="2")

    def test_negative_values(self):
        self.assertEqual(summarize_data(-10, 4, metric="sum"), -6)


if __name__ == "__main__":
    unittest.main()
