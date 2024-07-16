import datetime
import pandas as pd
from src.amortization_table_generator import amortization_table_generator

principal = 30000.0  # Loan amount
annual_interest_rate = 0.07  # Annual interest rate in percentage
term = 30  # Loan term in years
loan_start_date = datetime.date(2024, 8, 1)  # Loan start date

amortization_schedule = amortization_table_generator(principal, annual_interest_rate, term, monthly_payment=1000.0,
                                                     loan_start_date=loan_start_date)

pd.set_option('display.max_columns', None)  # Display all columns
pd.set_option('display.width', 1000)        # Increase the display width if needed

print(amortization_schedule)
