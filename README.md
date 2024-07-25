# amortization-calculator
## What is this?
- This python project generates an amortization schedule based on interest rate, loan term, principal amount and origination fee (if any).
- It also calculates the APR of the loan based on the amortization schedule.
## How is it different than any of the amortization calculators you can find on the internet?
- It is extremely precise. It takes into account the varying number of days in each month which affects how interest is accrued. Also, for each period, payments and balances are rounded to the nearest cent so you don't deal with a fraction of a cent.
- It aims to be compliant with the relevant regualtion. The APR calculation is done using the actuarial method set forth in appendix J of Regulation Z (Truth in Lending) which is implemented and enforced by the Consumer Financial Protection Bureau.
## How to use
1. Clone the project
2. Set up the virtual environment based on requirements.txt
3. Within the virtual environment, run the main.py with the expected parameters

`python .\main.py --principal 100000 --annual_interest_rate 0.05 --term 36 --loan_start_date 2024-07-02`

And you get an amortization schedule that looks like this:

|    | Date       |   Year_Fraction |   Principal_Payment |   Interest_Payment |   Fee_Payment |   Payment_Amount |   Balance |
|---:|:-----------|----------------:|--------------------:|-------------------:|--------------:|-----------------:|----------:|
|  0 | 2024-07-02 |       0         |                0    |               0    |             0 |             0    | 100000    |
|  1 | 2024-08-02 |       0.0846995 |             2573.7  |             423.5  |             0 |          2997.2  |  97426.3  |
|  2 | 2024-09-02 |       0.0846995 |             2584.6  |             412.6  |             0 |          2997.2  |  94841.7  |
|  3 | 2024-10-02 |       0.0819672 |             2608.5  |             388.7  |             0 |          2997.2  |  92233.2  |


...

It also yields a list of important loan metrics


`
Loan Metrics:
First_Payment_Date: 2024-08-02
First_Payment_Amount: 2997.2
Last_Payment_Date: 2027-07-02
Last_Payment_Amount: 2996.86
Finance_Charge: 7898.86
Total_of_Payments: 107898.86
Ending_Balance: 0.0
APR: 0.05002260829611073
`

## Assumptions
- First payment date
  - The first payment date is set to be same day of the second month of the loan start date, except for when the loan start date is on the 29th, 30th, or 31st in which case the first payment date is the first day of the third month of the loan start date.
- Day count conventions
  - The default is Actual/Actual but it also supports day count conventions like Actual/365 or Actual/360.
- Determination of monthly payment amount
  - The number of payments is set by the paramter `term` which includes `term`-1 of equal payments and a last payment which is no more than the first payment.
  - The calculator goes through an interative process to find the minimum first payment amount that meets the above criterion and makes sure the ending balance is zero.
- Handling of origination fee
  - The origination fee is deducted from the disbursement amount. 
- Interest payment and principal payment
  - For each payment period, the payment always goes to interest accrued first before it is applied agaisnt remaining principal balance.
