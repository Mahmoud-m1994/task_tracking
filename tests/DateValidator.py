import unittest
from datetime import datetime, timedelta
from utilities.DateValidator import (
    is_start_date_after_end_date_or_equal,
    is_date_in_past,
    is_existing_end_date_after_start_date,
    is_existing_end_date_after_end_date,
    is_existing_start_date_after_end_date,
)


class MyTestCase(unittest.TestCase):
    def test_is_start_date_after_end_date(self):
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2022, 12, 31)
        self.assertTrue(is_start_date_after_end_date_or_equal(start_date, end_date))

        start_date = datetime(2022, 12, 31)
        end_date = datetime(2023, 1, 1)
        self.assertFalse(is_start_date_after_end_date_or_equal(start_date, end_date))

        start_date = datetime(2022, 12, 31)
        end_date = datetime(2022, 12, 31)
        self.assertTrue(is_start_date_after_end_date_or_equal(start_date, end_date))

    def test_is_date_in_past(self):
        future_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        self.assertFalse(is_date_in_past(future_date))

        past_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        self.assertTrue(is_date_in_past(past_date))

    def test_is_existing_end_date_after_start_date(self):
        existing_end_date = "2023-01-01 00:00:00"
        new_start_date = "2022-12-31"
        self.assertTrue(is_existing_end_date_after_start_date(existing_end_date, new_start_date))

        existing_end_date = "2022-12-31 00:00:00"
        new_start_date = "2023-01-01"
        self.assertFalse(is_existing_end_date_after_start_date(existing_end_date, new_start_date))

        existing_end_date = "2023-01-01 00:00:00"
        new_start_date = "2023-01-01"
        self.assertTrue(is_existing_end_date_after_start_date(existing_end_date, new_start_date))

    def test_is_existing_end_date_after_end_date(self):
        existing_end_date = "2023-01-01 00:00:00"
        new_end_date = "2022-12-31"
        self.assertTrue(is_existing_end_date_after_end_date(existing_end_date, new_end_date))

        existing_end_date = "2022-12-31 00:00:00"
        new_end_date = "2023-01-01"
        self.assertFalse(is_existing_end_date_after_end_date(existing_end_date, new_end_date))

        existing_end_date = "2023-01-01 00:00:00"
        new_end_date = "2023-01-01"
        self.assertTrue(is_existing_end_date_after_end_date(existing_end_date, new_end_date))

    def test_is_existing_start_date_after_end_date(self):
        existing_start_date = "2023-01-01 00:00:00"
        new_end_date = "2022-12-31"
        self.assertTrue(is_existing_start_date_after_end_date(existing_start_date, new_end_date))

        existing_start_date = "2022-12-31 00:00:00"
        new_end_date = "2023-01-01"
        self.assertFalse(is_existing_start_date_after_end_date(existing_start_date, new_end_date))

if __name__ == '__main__':
    unittest.main()