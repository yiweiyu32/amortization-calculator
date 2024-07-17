from dateutil.relativedelta import relativedelta

from src.payment_table_calculator import amortization_table_calculator
from datetime import date
import numpy_financial as npf

zero_cent_threshold = 0.005
one_cent = 0.01
apr_increment = 0.001


def amortization_schedule_finder(principal: float, annual_interest_rate: float, term: int,
                                 loan_start_date: date, day_count_convention_name: str,
                                 origination_fee: float):
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

        length_first_period = relativedelta(first_payment_date, advance_date)

        num_unit_periods_in_first_period = length_first_period.years * 12 + length_first_period.months
        full_unit_period_start = first_payment_date - relativedelta(months=num_unit_periods_in_first_period)
        fraction_unit_period = (full_unit_period_start - advance_date).days / 30.0

        initial_guess_apr = npf.rate(num_of_payments, regular_payment, -amount_advanced, 0.0) * 12.0
        estimated_apr = initial_guess_apr

        def estimate_amount_advanced(apr):
            monthly_rate = apr / 12.0
            discount_start_to_first_unit_period = 1.0 / (1.0 + fraction_unit_period * monthly_rate)
            discount_first_unit_period_first_pmt = 1.0 / pow(1.0 + monthly_rate, num_unit_periods_in_first_period)
            discounted_final_payment = (regular_payment * (1.0 - 1.0 / pow(1.0 + monthly_rate, num_of_payments - 1)) /
                                        (1.0 - 1.0 / (1.0 + monthly_rate)))
            discounted_other_payments = final_payment / pow(1.0 + monthly_rate, num_of_payments - 1)
            return (discount_start_to_first_unit_period * discount_first_unit_period_first_pmt *
                    (discounted_final_payment + discounted_other_payments))

        estimated_apr_prime = estimated_apr + apr_increment
        estimated_amount_advanced = estimate_amount_advanced(estimated_apr)
        estimated_amount_advanced_prime = estimate_amount_advanced(estimated_apr_prime)
        new_estimated_apr = (estimated_apr + apr_increment * (amount_advanced - estimated_amount_advanced) /
                             (estimated_amount_advanced_prime - estimated_amount_advanced))
        tolerance_level = 0.000001

        while abs(new_estimated_apr - estimated_apr) > tolerance_level:
            # print(estimated_apr, estimated_apr_prime, new_estimated_apr)
            estimated_apr = new_estimated_apr
            estimated_apr_prime = estimated_apr + apr_increment
            estimated_amount_advanced = estimate_amount_advanced(estimated_apr)
            estimated_amount_advanced_prime = estimate_amount_advanced(estimated_apr_prime)
            new_estimated_apr = (estimated_apr + apr_increment * (amount_advanced - estimated_amount_advanced) /
                                 (estimated_amount_advanced_prime - estimated_amount_advanced))

        return estimated_apr

    # Find best first payment amount
    initial_guess = npf.pmt(rate=annual_interest_rate / 12.0, nper=term, pv=-principal)
    first_payment = round(initial_guess, 2)

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

    return amortization_schedule, loan_metrics_res, calculate_apr(loan_metrics_res)
