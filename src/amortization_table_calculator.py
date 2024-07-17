import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta

from src.day_count_convention import get_day_count_convention

zero_float = 0.0


def amortization_table_calculator(principal: float, annual_interest_rate: float, term: int,
                                  scheduled_monthly_payment: float,
                                  loan_start_date: date, day_count_convention_name: str = 'Actual/Actual',
                                  origination_fee: float = 0.0):

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

    dates.append(current_date)
    payment_amounts.append(payment_amount)
    principal_payments.append(zero_float)
    interest_payments.append(zero_float)
    principal_balances.append(principal)
    year_fractions.append(zero_float)
    fee_payments.append(origination_fee)

    if current_date.day > 28:
        next_date = (current_date + relativedelta(months=+2)).replace(day=1)
    else:
        next_date = current_date + relativedelta(months=+1)

    first_payment_date = next_date

    for _ in range(term):
        dates.append(next_date)

        day_count_convention = get_day_count_convention(day_count_convention_name, current_date, next_date)
        year_fraction = day_count_convention.year_fraction()
        year_fractions.append(year_fraction)

        # Calculate interest for the current month
        interest_accrued = balance * annual_interest_rate * year_fraction
        interest_payment = round(interest_accrued, 2)
        # Calculate principal payment for the current month
        principal_payment = round(min(scheduled_monthly_payment - interest_payment, balance), 2)

        # Update the balance
        balance = round(balance - principal_payment, 2)

        # Store details for the current month
        payment_amount = round(interest_payment + principal_payment, 2)
        payment_amounts.append(payment_amount)
        principal_payments.append(principal_payment)
        interest_payments.append(interest_payment)
        principal_balances.append(balance)
        fee_payments.append(zero_float)

        # Advance the date by one month
        current_date = next_date
        next_date = current_date + relativedelta(months=+1)

    last_payment = payment_amount

    # Create a DataFrame to store the amortization schedule
    amort_schedule = pd.DataFrame({
        "Date": dates,
        "Year_Fraction": year_fractions,
        "Principal_Payment": principal_payments,
        "Interest_Payment": interest_payments,
        "Fee_Payment": fee_payments,
        "Payment_Amount": payment_amounts,
        "Balance": principal_balances
    })

    finance_charge = round(sum(interest_payments) + sum(fee_payments), 2)
    total_of_payments = round(sum(payment_amounts), 2)

    loan_metrics = {
        "First_Payment_Date": first_payment_date,
        "Last_Payment": last_payment,
        "Finance_Charge": finance_charge,
        "Total_of_Payments": total_of_payments,
        "Ending_Balance": balance
    }
    return amort_schedule, loan_metrics
