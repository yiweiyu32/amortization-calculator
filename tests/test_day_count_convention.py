import unittest
from datetime import date

from src.day_count_convention import Actual360, Actual365, ActualActual, get_day_count_convention


class TestDayCountConventions(unittest.TestCase):

    def test_days_between(self):
        dcc = Actual360(start_date=date(2024, 1, 1), end_date=date(2025, 1, 1))
        self.assertEqual(dcc.days_between(), 366)

    def test_actual360(self):
        dcc = Actual360(start_date=date(2024, 1, 1), end_date=date(2025, 1, 31))
        self.assertAlmostEqual(dcc.year_fraction(), 396 / 360, places=6)

    def test_actual365(self):
        dcc = Actual365(start_date=date(2023, 1, 1), end_date=date(2023, 12, 31))
        self.assertAlmostEqual(dcc.year_fraction(), 364 / 365, places=6)

    def test_actualactual_same_year(self):
        dcc = ActualActual(start_date=date(2023, 1, 1), end_date=date(2023, 12, 31))
        self.assertAlmostEqual(dcc.year_fraction(), 364 / 365, places=6)

    def test_actualactual_different_years(self):
        dcc = ActualActual(start_date=date(2023, 12, 31), end_date=date(2024, 1, 2))
        self.assertAlmostEqual(dcc.year_fraction(), 1 / 365 + 1 / 366, places=6)

    def test_actualactual_leap_year_start(self):
        """Test ActualActual where the period starts in a leap year."""
        dcc = ActualActual(start_date=date(2016, 12, 31), end_date=date(2021, 1, 2))
        # Dec 31, 2020 (leap year) + Jan 1, 2021 and Jan 2, 2021 (normal year)
        expected_fraction = 1 / 366 + 1 / 365 + 4
        self.assertAlmostEqual(dcc.year_fraction(), expected_fraction, places=6)

    def test_actualactual_leap_year_end(self):
        """Test ActualActual where the period ends in a leap year."""
        dcc = ActualActual(start_date=date(2018, 12, 31), end_date=date(2020, 1, 2))
        # Dec 31, 2019 (normal year) + Jan 1, 2020 and Jan 2, 2020 (leap year)
        expected_fraction = 1 / 365 + 1 / 366 + 1
        self.assertAlmostEqual(dcc.year_fraction(), expected_fraction, places=6)

    def test_get_day_count_convention(self):
        dcc = get_day_count_convention('Actual/360', date(2023, 1, 1), date(2023, 12, 31))
        self.assertIsInstance(dcc, Actual360)
        dcc = get_day_count_convention('Actual/365', date(2023, 1, 1), date(2023, 12, 31))
        self.assertIsInstance(dcc, Actual365)
        dcc = get_day_count_convention('Actual/Actual', date(2023, 1, 1), date(2023, 12, 31))
        self.assertIsInstance(dcc, ActualActual)

    def test_get_day_count_convention_invalid(self):
        with self.assertRaises(ValueError):
            get_day_count_convention('Invalid/Convention', date(2023, 1, 1), date(2023, 12, 31))


if __name__ == '__main__':
    unittest.main()