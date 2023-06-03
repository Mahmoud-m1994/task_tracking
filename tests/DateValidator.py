import unittest
from datetime import datetime
from utilities.DateValidator import is_start_date_after_end_date_or_equal


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


if __name__ == '__main__':
    unittest.main()
