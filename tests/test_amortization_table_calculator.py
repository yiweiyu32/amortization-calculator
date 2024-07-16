from datetime import date
import pandas as pd
from src.amortization_table_calculator import amortization_table_calculator

principal = 10000.0  # Loan amount
annual_interest_rate = 0.1381  # Annual interest rate in percentage
term = 60  # Loan term in years
loan_start_date = date(2024, 7, 2)  # Loan start date

amortization_schedule, loan_metrics = (
    amortization_table_calculator(principal, annual_interest_rate, term,
                                  scheduled_monthly_payment=231.73,
                                  loan_start_date=loan_start_date,
                                  origination_fee=000.0
                                  ))

pd.set_option('display.max_columns', None)  # Display all columns
pd.set_option('display.width', 1000)  # Increase the display width if needed
pd.set_option('display.max_rows', None)

print(amortization_schedule)
print(loan_metrics)
