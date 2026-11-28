"""Automated tests for the learner's NLP Text Data Quality Pipeline."""
import copy
import unittest
from pipeline import validate_review, normalize_text, process_reviews, reviews


class ValidateReviewTests(unittest.TestCase):
    def test_valid_text(self):
        self.assertTrue(validate_review({'id': 1, 'text': 'Good'}))
        self.assertTrue(validate_review({'id': 2, 'text': '  Good  '}))

    def test_invalid_non_dict(self):
        for value in (None, [], 'hello', 12):
            with self.subTest(value=value):
                self.assertFalse(validate_review(value))

    def test_missing_keys(self):
        for value in ({'id': 1}, {'text': 'Good'}, {}):
            with self.subTest(value=value):
                self.assertFalse(validate_review(value))

    def test_invalid_ids(self):
        for value in (0, -5, '7', True, False, 2.5, None):
            with self.subTest(value=value):
                self.assertFalse(validate_review({'id': value, 'text': 'Good'}))

    def test_invalid_texts(self):
        for value in ('', ' \t\n ', None, 12345, ['hi']):
            with self.subTest(value=value):
                self.assertFalse(validate_review({'id': 1, 'text': value}))

    def test_validation_no_mutation(self):
        item = {'id': 9, 'text': '  Good  '}
        before = copy.deepcopy(item)
        validate_review(item)
        self.assertEqual(item, before)


class NormalizeTextTests(unittest.TestCase):
    def test_separators_and_punctuation(self):
        self.assertEqual(normalize_text('VERY-GOOD_product!!!'), 'very good product')

    def test_contractions_case_insensitive(self):
        self.assertEqual(normalize_text("I CAN'T recommend it!"), 'i cannot recommend it')
        self.assertEqual(normalize_text("This ISN'T good."), 'this is not good')

    def test_unicode_casefold(self):
        self.assertEqual(normalize_text('Straße   PRODUCT!!!'), 'strasse product')

    def test_whitespace_normalization(self):
        self.assertEqual(normalize_text('  Fast\t delivery \n great   service  '), 'fast delivery great service')

    def test_input_string_unchanged(self):
        raw = 'VERY-GOOD product!!!'
        normalize_text(raw)
        self.assertEqual(raw, 'VERY-GOOD product!!!')

    def test_all_expected_valid_reviews(self):
        expected = {
            1: 'very good product', 2: 'very good product',
            3: 'i cannot recommend it', 4: 'the product is not working',
            5: 'fast delivery great service', 8: 'amazing quality',
            9: 'amazing quality', 10: 'poor customer support',
            12: 'not bad but expensive'
        }
        for record in reviews:
            if record['id'] in expected:
                with self.subTest(id=record['id']):
                    self.assertEqual(normalize_text(record['text']), expected[record['id']])


class ProcessReviewsTests(unittest.TestCase):
    def test_main_dataset_counts(self):
        report = process_reviews(reviews)
        self.assertEqual((report['total_records'], report['total_clean'], report['total_invalid'], report['total_duplicates']), (12, 7, 3, 2))

    def test_main_dataset_duplicate_ids(self):
        self.assertEqual(process_reviews(reviews)['duplicate_ids'], [2, 9])

    def test_main_dataset_invalid_order(self):
        self.assertEqual([r['id'] for r in process_reviews(reviews)['invalid_reviews']], [6, 7, 11])

    def test_main_dataset_clean_records_and_order(self):
        expected = [
            {'id': 1, 'text': 'very good product'},
            {'id': 3, 'text': 'i cannot recommend it'},
            {'id': 4, 'text': 'the product is not working'},
            {'id': 5, 'text': 'fast delivery great service'},
            {'id': 8, 'text': 'amazing quality'},
            {'id': 10, 'text': 'poor customer support'},
            {'id': 12, 'text': 'not bad but expensive'},
        ]
        self.assertEqual(process_reviews(reviews)['clean_reviews'], expected)

    def test_empty_input(self):
        report = process_reviews([])
        self.assertEqual((report['total_records'], report['total_clean'], report['total_invalid'], report['total_duplicates']), (0, 0, 0, 0))
        for key in ('clean_reviews', 'invalid_reviews', 'duplicate_ids'):
            self.assertEqual(report[key], [])

    def test_deduplicate_casefold_and_whitespace(self):
        items = [{'id': 1, 'text': '  Straße  '}, {'id': 2, 'text': 'STRASSE'}, {'id': 3, 'text': 'hello   WORLD'}, {'id': 4, 'text': 'hello world'}]
        report = process_reviews(items)
        self.assertEqual(report['duplicate_ids'], [2, 4])
        self.assertEqual([r['id'] for r in report['clean_reviews']], [1, 3])

    def test_does_not_mutate_input(self):
        original = copy.deepcopy(reviews)
        process_reviews(reviews)
        self.assertEqual(reviews, original)

    def test_no_valid_records(self):
        data = [{'id': 1, 'text': None}, {'id': 2, 'text': '   '}]
        report = process_reviews(data)
        self.assertEqual((report['total_clean'], report['total_invalid'], report['total_duplicates']), (0, 2, 0))

    def test_invalid_non_dict_record(self):
        data = [None, {'id': 2, 'text': 'Good'}]
        report = process_reviews(data)
        self.assertEqual(report['invalid_reviews'], [None])
        self.assertEqual(report['clean_reviews'], [{'id': 2, 'text': 'good'}])


if __name__ == '__main__':
    unittest.main(verbosity=2)
