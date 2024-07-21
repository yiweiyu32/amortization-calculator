from datetime import date
from src.payment_table_calculator import amortization_table_calculator
import unittest


class TestAmortizationCalculator(unittest.TestCase):

    def setUp(self):
        # Initialize common parameters for tests
        self.principal = 200000.0
        self.annual_interest_rate = 0.1381
        self.term = 60
        self.scheduled_monthly_payment = 231.73
        self.loan_start_date = date(2024, 1, 29)
        self.day_count_convention_name = 'Actual/Actual'
        self.origination_fee = 0.0

    def test_amortization_schedule(self):
        # Test the amortization schedule calculation
        amort_schedule, loan_metrics = amortization_table_calculator(
            self.principal, self.annual_interest_rate, self.term,
            self.scheduled_monthly_payment, self.loan_start_date,
            self.day_count_convention_name, self.origination_fee
        )

        # Check that the amortization schedule DataFrame has the expected columns
        expected_columns = [
            "Date", "Year_Fraction", "Principal_Payment", "Interest_Payment",
            "Fee_Payment", "Payment_Amount", "Balance"
        ]
        self.assertEqual(list(amort_schedule.columns), expected_columns)

        # Check that the length of the schedule matches the term
        self.assertEqual(len(amort_schedule), self.term + 1)

    def test_loan_metrics(self):
        # Test the loan metrics calculation
        _, loan_metrics = amortization_table_calculator(
            self.principal, self.annual_interest_rate, self.term,
            self.scheduled_monthly_payment, self.loan_start_date,
            self.day_count_convention_name, self.origination_fee
        )

        # Check that the loan metrics dictionary has the expected keys
        expected_keys = [
            "First_Payment_Date", "First_Payment_Amount", "Last_Payment_Date", "Last_Payment_Amount", "Finance_Charge",
            "Total_of_Payments", "Ending_Balance"
        ]
        self.assertEqual(list(loan_metrics.keys()), expected_keys)

        # Check that finance charge and total of payments are positive
        self.assertGreaterEqual(loan_metrics["Finance_Charge"], 0)
        self.assertGreaterEqual(loan_metrics["Total_of_Payments"], 0)
        self.assertGreaterEqual(loan_metrics["Ending_Balance"], 0)

        self.assertEqual(loan_metrics["First_Payment_Date"], date(2024, 3, 1))


if __name__ == '__main__':
    unittest.main()
