import time
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta

from src.day_count_convention import get_day_count_convention
from src.helpers import round_fast

zero_float_type = 0.0


def amortization_table_calculator(principal: float, annual_interest_rate: float, term: int,
                                  scheduled_monthly_payment: float,
                                  loan_start_date: date, day_count_convention_name: str,
                                  origination_fee: float):
    # Initialize lists to store the schedule details
    dates = []
    payment_amounts = []
    principal_payments = []
    interest_payments = []
    principal_balances = []
    fee_payments = []
    year_fractions = []

    # Initial balance is the principal
    balance = principal
    current_date = loan_start_date
    payment_amount = origination_fee

    # Append first entries to the lists
    dates.append(current_date)
    payment_amounts.append(payment_amount)
    principal_payments.append(zero_float_type)
    interest_payments.append(zero_float_type)
    principal_balances.append(principal)
    year_fractions.append(zero_float_type)
    fee_payments.append(origination_fee)

    # The first payment date should be the same day next month, except for when the day is >28
    if current_date.day > 28:
        next_date = (current_date + relativedelta(months=+2)).replace(day=1)
    else:
        next_date = current_date + relativedelta(months=+1)

    first_payment_date = next_date

    for _ in range(term):
        # Calculate year fraction based on day count convention
        day_count_convention = get_day_count_convention(day_count_convention_name, current_date, next_date)
        year_fraction = day_count_convention.year_fraction()

        # Calculate interest for the current month
        interest_accrued = balance * annual_interest_rate * year_fraction
        interest_payment = round_fast(interest_accrued, 2)

        # Calculate principal payment for the current month
        principal_payment = round_fast(min(scheduled_monthly_payment - interest_payment, balance), 2)

        # Update the balance
        balance = round_fast(balance - principal_payment, 2)

        # Calculate payment amount
        payment_amount = round_fast(interest_payment + principal_payment, 2)

        # Store details for the current month
        dates.append(next_date)
        year_fractions.append(year_fraction)
        payment_amounts.append(payment_amount)
        principal_payments.append(principal_payment)
        interest_payments.append(interest_payment)
        principal_balances.append(balance)
        fee_payments.append(zero_float_type)

        # Advance the date by one month
        current_date = next_date

        year_temp = current_date.year
        month_temp = current_date.month

        if month_temp == 12:
            year_temp += 1
            month_temp = 1
        else:
            month_temp += 1

        next_date = date(year_temp, month_temp, current_date.day)

    # Calculate loan metrics
    last_payment = payment_amount
    last_payment_date = current_date
    finance_charge = round_fast(sum(interest_payments) + sum(fee_payments), 2)
    total_of_payments = round_fast(sum(payment_amounts), 2)

    loan_metrics = {
        "First_Payment_Date": first_payment_date,
        "First_Payment_Amount": scheduled_monthly_payment,
        "Last_Payment_Date": last_payment_date,
        "Last_Payment_Amount": last_payment,
        "Finance_Charge": finance_charge,
        "Total_of_Payments": total_of_payments,
        "Ending_Balance": balance
    }

    amort_schedule = pd.DataFrame({
        "Date": dates,
        "Year_Fraction": year_fractions,
        "Principal_Payment": principal_payments,
        "Interest_Payment": interest_payments,
        "Fee_Payment": fee_payments,
        "Payment_Amount": payment_amounts,
        "Balance": principal_balances
    })
    return amort_schedule, loan_metrics
