from datetime import date
from src.amortization_schedule_finder import find_first_payment

principal = 10000.0  # Loan amount
annual_interest_rate = 0.1381  # Annual interest rate in percentage
term = 60  # Loan term in years
loan_start_date = date(2024, 7, 2)  # Loan start date

amortization_schedule, first_payment = \
    find_first_payment(principal=principal, annual_interest_rate=annual_interest_rate, term=term,
                       loan_start_date=loan_start_date)

# print("result")
print(amortization_schedule, first_payment)
