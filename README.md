# amortization-calculator
## What is this?
* This python project generates an amortization schedule based on provided interest rate, loan term, principal and origination fee (if any)
* It also calculates the APR of the loan in accordance with the actuarial method set forth in appendix J of Regulation Z (Truth in Lending) which is implemented and enforced by the Consumer Financial Protection Bureau
## How to use
Within the virtual environment

`python .\main.py --principal 100000 --annual_interest_rate 0.05 --term 36 --loan_start_date 2024-07-02`

And you get

`Amortization Schedule:`
|    | Date       |   Year_Fraction |   Principal_Payment |   Interest_Payment |   Fee_Payment |   Payment_Amount |   Balance |
|---:|:-----------|----------------:|--------------------:|-------------------:|--------------:|-----------------:|----------:|
|  0 | 2024-07-02 |       0         |                0    |               0    |             0 |             0    | 100000    |
|  1 | 2024-08-02 |       0.0846995 |             2573.7  |             423.5  |             0 |          2997.2  |  97426.3  |
|  2 | 2024-09-02 |       0.0846995 |             2584.6  |             412.6  |             0 |          2997.2  |  94841.7  |
|  3 | 2024-10-02 |       0.0819672 |             2608.5  |             388.7  |             0 |          2997.2  |  92233.2  |


...

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
* First payment date
* Interest accrual method
* Determination of monthly payment amount
* Handling of origination fee
* Interest payment and principal payment
* Payment amount
