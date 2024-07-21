from datetime import date
from dateutil.relativedelta import relativedelta
import numpy_financial as npf

from src.helpers import round_fast
from src.payment_table_calculator import amortization_table_calculator

ZERO_CENT_THRESHOLD = 0.005
ONE_CENT = 0.01
APR_INCREMENT = 0.001
TOLERANCE_LEVEL = 0.000001


def amortization_schedule_finder(principal: float, annual_interest_rate: float,
                                 term: int, loan_start_date: date,
                                 day_count_convention_name: str,
                                 origination_fee: float):
    def get_amort_table_n_loan_metrics(scheduled_monthly_payment):
        amort_schedule, loan_metrics = amortization_table_calculator(
            principal=principal, annual_interest_rate=annual_interest_rate,
            term=term, loan_start_date=loan_start_date,
            day_count_convention_name=day_count_convention_name,
            origination_fee=origination_fee,
            scheduled_monthly_payment=scheduled_monthly_payment)
        return amort_schedule, loan_metrics

    def calculate_apr(loan_metrics):
        # (3) Single advance transaction, with an odd final payment, with or without an odd first 
        # period, and otherwise regular.

        amount_advanced = principal - origination_fee
        regular_payment = loan_metrics.get("First_Payment_Amount")
        final_payment = loan_metrics.get("Last_Payment_Amount")
        first_payment_date = loan_metrics.get("First_Payment_Date")

        length_first_period = relativedelta(first_payment_date, loan_start_date)

        num_up_t = length_first_period.years * 12 + length_first_period.months
        full_unit_period_start = first_payment_date - relativedelta(months=num_up_t)
        fraction_unit_period = (full_unit_period_start - loan_start_date).days / 30.0

        initial_guess_apr = npf.rate(term, regular_payment, -amount_advanced, 0.0) * 12.0
        estimated_apr = initial_guess_apr

        def estimate_amount_advanced(apr):
            monthly_rate = apr / 12.0
            discount_start_to_first_unit_period = 1.0 / (1.0 + fraction_unit_period * monthly_rate)
            discount_first_unit_period_first_pmt = 1.0 / pow(1.0 + monthly_rate, num_up_t)
            discounted_final_payment = (regular_payment * (1.0 - 1.0 / pow(1.0 + monthly_rate, term - 1)) /
                                        (1.0 - 1.0 / (1.0 + monthly_rate)))
            discounted_other_payments = final_payment / pow(1.0 + monthly_rate, term - 1)
            return (discount_start_to_first_unit_period * discount_first_unit_period_first_pmt *
                    (discounted_final_payment + discounted_other_payments))

        def update_apr(apr):
            apr_prime = apr + APR_INCREMENT
            estimated_amount_advanced = estimate_amount_advanced(apr)
            estimated_amount_advanced_prime = estimate_amount_advanced(apr_prime)
            new_apr = apr + APR_INCREMENT * (amount_advanced - estimated_amount_advanced) / (
                        estimated_amount_advanced_prime - estimated_amount_advanced)
            return new_apr

        new_estimated_apr = update_apr(estimated_apr)

        while abs(new_estimated_apr - estimated_apr) > TOLERANCE_LEVEL:
            estimated_apr = new_estimated_apr
            new_estimated_apr = update_apr(new_estimated_apr)

        return estimated_apr

    # Find best first payment amount
    initial_guess = npf.pmt(rate=annual_interest_rate / 12.0, nper=term, pv=-principal)
    first_payment = round(initial_guess, 2)

    # start_time = time.time()

    _, loan_metrics_res = get_amort_table_n_loan_metrics(first_payment)
    _, loan_metrics_prime = get_amort_table_n_loan_metrics(first_payment - ONE_CENT)

    ending_balance = loan_metrics_res.get("Ending_Balance")
    last_payment = loan_metrics_res.get("Last_Payment_Amount")
    ending_balance_prime = loan_metrics_prime.get("Ending_Balance")

    while ending_balance > ZERO_CENT_THRESHOLD or ending_balance_prime < ZERO_CENT_THRESHOLD:
        if ending_balance > ZERO_CENT_THRESHOLD:
            first_payment = round_fast(first_payment +
                                       max(ending_balance / term * 0.5, ONE_CENT), 2)
        if ending_balance_prime < ZERO_CENT_THRESHOLD:
            first_payment = round_fast(first_payment -
                                       max((first_payment - last_payment) / term * 0.5, ONE_CENT), 2)
        _, loan_metrics_res = get_amort_table_n_loan_metrics(first_payment)
        _, loan_metrics_prime = get_amort_table_n_loan_metrics(first_payment - ONE_CENT)

        ending_balance = loan_metrics_res.get("Ending_Balance")
        last_payment = loan_metrics_res.get("Last_Payment_Amount")
        ending_balance_prime = loan_metrics_prime.get("Ending_Balance")

    amortization_schedule, _ = get_amort_table_n_loan_metrics(first_payment)

    calculated_apr = calculate_apr(loan_metrics_res)

    return amortization_schedule, loan_metrics_res, calculated_apr
