import argparse
from datetime import date
import tabulate
from src.amortization_schedule_finder import amortization_schedule_finder


def main():
    parser = argparse.ArgumentParser(description="Amortization Schedule Calculator")

    parser.add_argument('--principal', type=float, required=True, help='Loan principal amount')
    parser.add_argument('--annual_interest_rate', type=float, required=True, help='Annual interest rate in decimal')
    parser.add_argument('--term', type=int, required=True, help='Loan term in months')
    parser.add_argument('--loan_start_date', type=str, required=True, help='Loan start date in YYYY-MM-DD format')
    parser.add_argument('--day_count_convention', type=str, default='Actual/Actual',
                        help='Day count convention (default: Actual/Actual)')
    parser.add_argument('--origination_fee', type=float, default=0.0, help='Origination fee (default: 0.0)')

    args = parser.parse_args()

    # Parse the loan start date
    loan_start_date = date.fromisoformat(args.loan_start_date)

    # Calculate the amortization schedule
    schedule, metrics, apr = amortization_schedule_finder(
        principal=args.principal,
        annual_interest_rate=args.annual_interest_rate,
        term=args.term,
        loan_start_date=loan_start_date,
        day_count_convention_name=args.day_count_convention,
        origination_fee=args.origination_fee
    )

    # Print the amortization schedule
    print("Amortization Schedule:")
    print(schedule.to_markdown())

    # Print the loan metrics
    print("\nLoan Metrics:")
    for key, value in metrics.items():
        print(f"{key}: {value}")

    print("APR: " + f"{apr}")


if __name__ == '__main__':
    main()
    input("Press Enter to exit...")
