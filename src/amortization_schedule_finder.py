from src.amortization_table_calculator import amortization_table_calculator
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

    amortization_schedule, loan_metrics_current = get_amort_schedule_n_loan_metrics(first_payment)
    _, loan_metrics_prime = get_amort_schedule_n_loan_metrics(first_payment - one_cent)

    ending_balance = loan_metrics_current.get("Ending_Balance")
    last_payment = loan_metrics_current.get("Last_Payment_Amount")
    ending_balance_prime = loan_metrics_prime.get("Ending_Balance")

    while ending_balance > zero_cent_threshold or ending_balance_prime < zero_cent_threshold:
        if ending_balance > zero_cent_threshold:
            first_payment = round(first_payment + max(ending_balance / term, one_cent), 2)
        if ending_balance_prime < zero_cent_threshold:
            first_payment = round(first_payment - max((first_payment - last_payment) / term, one_cent), 2)
        amortization_schedule, loan_metrics_current = get_amort_schedule_n_loan_metrics(first_payment)
        _, loan_metrics_prime = get_amort_schedule_n_loan_metrics(first_payment - one_cent)

        ending_balance = loan_metrics_current.get("Ending_Balance")
        last_payment = loan_metrics_current.get("Last_Payment_Amount")
        ending_balance_prime = loan_metrics_prime.get("Ending_Balance")

    return amortization_schedule, loan_metrics_current
