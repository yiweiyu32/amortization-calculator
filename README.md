# amortization-calculator
## This calculator does a couple of things
* It generates an amortization schedule based on provided interest rate, loan term, principal and origination fee (if any)
* It calculates the APR of the loan in accordance with the actuarial method set forth in appendix J of Regulation Z (Truth in Lending) which is implemented and enforced by the Consumer Financial Protection Bureau
## Assumptions
* First payment date
* Interest accrual method
* Determination of monthly payment amount
* Handling of origination fee
* Interest payment and principal payment
* Payment amount
## How to use
Within the virtual environment

`python .\main.py --principal 100000 --annual_interest_rate 0.05 --term 36 --loan_start_date 2024-07-02`

And you get

`
Amortization Schedule:
      Date  Year_Fraction  Principal_Payment  Interest_Payment  Fee_Payment  Payment_Amount   Balance
2024-07-02       0.000000               0.00              0.00          0.0            0.00 100000.00
2024-08-02       0.084699            2573.70            423.50          0.0         2997.20  97426.30
2024-09-02       0.084699            2584.60            412.60          0.0         2997.20  94841.70
2024-10-02       0.081967            2608.50            388.70          0.0         2997.20  92233.20
...
`
