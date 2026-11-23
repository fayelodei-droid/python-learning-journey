"""Standard-library tests; run with: python -m unittest discover -s tests -v"""
import copy
import unittest

from main import events, validate_event, extract_features, process_events


class TestValidation(unittest.TestCase):
    def test_valid_event(self):
        self.assertTrue(validate_event(events[0]))

    def test_invalid_timestamp(self):
        self.assertFalse(validate_event(events[1]))
        self.assertFalse(validate_event(events[3]))

    def test_missing_keys(self):
        self.assertFalse(validate_event({"id": 10, "value": 150}))
        self.assertFalse(validate_event({"timestamp": events[0]["timestamp"], "value": 150}))
        self.assertFalse(validate_event({"id": 10, "timestamp": events[0]["timestamp"]}))

    def test_wrong_types_and_boolean(self):
        for field, value in [("id", True), ("value", False), ("id", "1"), ("value", "120")]:
            with self.subTest(field=field, value=value):
                event = {**events[0], field: value}
                self.assertFalse(validate_event(event))

    def test_timezone_is_required(self):
        self.assertFalse(validate_event({**events[0], "timestamp": "2026-07-15T12:00:00"}))


class TestFeatures(unittest.TestCase):
    def test_dst_fold_and_features(self):
        self.assertEqual(extract_features(events[2]), {
            "id": 3, "value": 200, "local_hour": 3, "weekday": 6,
            "is_weekend": 1, "fold": 1,
        })

    def test_regular_features(self):
        self.assertEqual(extract_features(events[0]), {
            "id": 1, "value": 120, "local_hour": 15, "weekday": 2,
            "is_weekend": 0, "fold": 0,
        })


class TestPipeline(unittest.TestCase):
    def test_counts_and_average(self):
        report = process_events(events)
        self.assertEqual(report["total_clean"], 3)
        self.assertEqual(report["total_invalid"], 2)
        self.assertAlmostEqual(report["average_value"], 470 / 3)
        self.assertEqual([e["id"] for e in report["clean_events"]], [1, 3, 5])
        self.assertEqual([e["id"] for e in report["invalid_events"]], [2, 4])

    def test_empty_events(self):
        report = process_events([])
        self.assertEqual(report["total_clean"], 0)
        self.assertEqual(report["total_invalid"], 0)
        self.assertEqual(report["average_value"], 0.0)

    def test_input_is_not_mutated(self):
        before = copy.deepcopy(events)
        process_events(events)
        self.assertEqual(events, before)


if __name__ == "__main__":
    unittest.main()
