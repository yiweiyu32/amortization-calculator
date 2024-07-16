import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta


def amortization_table_generator(principal: float, annual_interest_rate: float, term: int, monthly_payment: float,
                                 loan_start_date: datetime.date, origination_fee: float = 0.0):
    # Convert annual interest rate to monthly interest rate

    monthly_interest_rate = annual_interest_rate / 12

    # Initialize lists to store the schedule details
    payment_dates = []
    payment_amounts = []
    principal_payments = []
    interest_payments = []
    principal_balances = []

    # Initial balance is the principal
    balance = principal
    current_date = loan_start_date

    for _ in range(term):
        # Calculate interest for the current month
        interest_payment = balance * monthly_interest_rate
        # Calculate principal payment for the current month
        principal_payment = monthly_payment - interest_payment

        # Update the balance
        balance -= principal_payment

        # Store details for the current month
        payment_dates.append(current_date)

        payment_amounts.append(monthly_payment)
        principal_payments.append(principal_payment)
        interest_payments.append(interest_payment)
        principal_balances.append(balance)

        # Move to the next month
        if current_date.day > 28:
            current_date = (current_date + relativedelta(months=+1)).replace(day=1) + relativedelta(days=-1)
        else:
            current_date += relativedelta(months=+1)

        # Create a DataFrame to store the amortization schedule
        amort_schedule = pd.DataFrame({
            "Payment Date": payment_dates,
            "Payment Amount": payment_amounts,
            "Principal Payment": principal_payments,
            "Interest Payment": interest_payments,
            "Balance": principal_balances
        })

    return amort_schedule

