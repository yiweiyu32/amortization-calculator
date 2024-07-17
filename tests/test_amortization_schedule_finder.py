from datetime import date
import unittest
from src.amortization_schedule_finder import amortization_schedule_finder


class TestAmortizationScheduleFinder(unittest.TestCase):

    def setUp(self):
        # Initialize common parameters for tests
        self.principal = 10000.0
        self.annual_interest_rate = 0.1381
        self.term = 60
        self.loan_start_date = date(2024, 7, 2)
        self.day_count_convention_name = 'Actual/Actual'
        self.origination_fee = 300.0

    def test_amortization_schedule_finder(self):
        # Test the amortization schedule finder function
        amort_schedule, loan_metrics_current, apr = amortization_schedule_finder(
            self.principal, self.annual_interest_rate, self.term,
            self.loan_start_date, self.day_count_convention_name, self.origination_fee
        )

        # Check that the amortization schedule DataFrame has the expected columns
        expected_columns = [
            "Date", "Year_Fraction", "Principal_Payment", "Interest_Payment",
            "Fee_Payment", "Payment_Amount", "Balance"
        ]
        self.assertEqual(list(amort_schedule.columns), expected_columns)

        # Check that the length of the schedule matches the term
        self.assertEqual(len(amort_schedule), self.term + 1)

        # Check that the ending balance is close to zero
        self.assertAlmostEqual(loan_metrics_current["Ending_Balance"], 0.0, places=2)
        self.assertAlmostEqual(loan_metrics_current["First_Payment_Amount"], 231.73, places=2)
        self.assertAlmostEqual(loan_metrics_current["Finance_Charge"], 4203.44, places=2)
        self.assertAlmostEqual(loan_metrics_current["Total_of_Payments"], 14203.44, places=2)
        self.assertAlmostEqual(apr, 0.15189, places=5)


if __name__ == '__main__':
    unittest.main()
