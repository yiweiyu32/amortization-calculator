from dateutil.relativedelta import relativedelta

from src.payment_table_calculator import amortization_table_calculator
from datetime import date
import numpy_financial as npf

zero_cent_threshold = 0.005
one_cent = 0.01


def amortization_schedule_finder(principal: float, annual_interest_rate: float, term: int,
                                 loan_start_date: date, day_count_convention_name: str,
                                 origination_fee: float):
    initial_guess = npf.pmt(rate=annual_interest_rate / 12.0, nper=term, pv=-principal)
    first_payment = round(initial_guess, 2)

    def get_amort_schedule_n_loan_metrics(scheduled_monthly_payment):
        amort_schedule, loan_metrics = \
            amortization_table_calculator(principal=principal, annual_interest_rate=annual_interest_rate, term=term,
                                          loan_start_date=loan_start_date,
                                          day_count_convention_name=day_count_convention_name,
                                          origination_fee=origination_fee,
                                          scheduled_monthly_payment=scheduled_monthly_payment)
        return amort_schedule, loan_metrics

    def calculate_apr(loan_metrics):
        # (3) Single advance transaction, with an odd final payment, with or without an odd first period,
        # and otherwise regular.

        amount_advanced = principal - origination_fee
        regular_payment = loan_metrics.get("First_Payment_Amount")
        final_payment = loan_metrics.get("Last_Payment_Amount")
        num_of_payments = term
        advance_date = loan_start_date
        first_payment_date = loan_metrics.get("First_Payment_Date")

        delta = relativedelta(first_payment_date, advance_date)

        num_unit_periods_in_first_period = delta.years * 12 + delta.months
        full_unit_period_start = first_payment_date - relativedelta(months=num_unit_periods_in_first_period)
        fraction_unit_period = (full_unit_period_start - advance_date).days / 30.0

        print(num_of_payments, regular_payment, amount_advanced)

        initial_guess_apr = npf.rate(num_of_payments, regular_payment, -amount_advanced, 0.0) * 12.0
        apr = initial_guess_apr

        # TODO: finish apr calculation. Calculate discounted cash flow. Define convergence criteria.

        return apr

    amortization_schedule, loan_metrics_res = get_amort_schedule_n_loan_metrics(first_payment)
    _, loan_metrics_prime = get_amort_schedule_n_loan_metrics(first_payment - one_cent)

    ending_balance = loan_metrics_res.get("Ending_Balance")
    last_payment = loan_metrics_res.get("Last_Payment_Amount")
    ending_balance_prime = loan_metrics_prime.get("Ending_Balance")

    while ending_balance > zero_cent_threshold or ending_balance_prime < zero_cent_threshold:
        if ending_balance > zero_cent_threshold:
            first_payment = round(first_payment + max(ending_balance / term, one_cent), 2)
        if ending_balance_prime < zero_cent_threshold:
            first_payment = round(first_payment - max((first_payment - last_payment) / term, one_cent), 2)
        amortization_schedule, loan_metrics_res = get_amort_schedule_n_loan_metrics(first_payment)
        _, loan_metrics_prime = get_amort_schedule_n_loan_metrics(first_payment - one_cent)

        ending_balance = loan_metrics_res.get("Ending_Balance")
        last_payment = loan_metrics_res.get("Last_Payment_Amount")
        ending_balance_prime = loan_metrics_prime.get("Ending_Balance")

    print(calculate_apr(loan_metrics_res))

    return amortization_schedule, loan_metrics_res
