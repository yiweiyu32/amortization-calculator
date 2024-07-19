import calendar
from datetime import date


class DayCountConvention:
    """Class representing day count convention"""
    def __init__(self, start_date: date, end_date: date):
        self.start_date = start_date
        self.end_date = end_date

    def year_fraction(self) -> float:
        """Calculate the year fraction according to the day count convention."""
        raise NotImplementedError("Must implement year_fraction method")

    def days_between(self) -> int:
        """Calculate the number of days between the start and end dates."""
        return (self.end_date - self.start_date).days


class Actual360(DayCountConvention):
    def year_fraction(self) -> float:
        return self.days_between() / 360


class Actual365(DayCountConvention):
    def year_fraction(self) -> float:
        return self.days_between() / 365


class ActualActual(DayCountConvention):
    def year_fraction(self) -> float:
        start_year = self.start_date.year
        end_year = self.end_date.year

        start_year_days_in_year = 366 if calendar.isleap(start_year) else 365
        end_year_days_in_year = 366 if calendar.isleap(end_year) else 365

        if start_year == end_year:
            return self.days_between() / start_year_days_in_year
        else:
            start_year_days = (date(start_year + 1, 1, 1) - self.start_date).days
            end_year_days = (self.end_date - date(end_year, 1, 1)).days

            start_year_fraction = start_year_days / start_year_days_in_year
            end_year_fraction = end_year_days / end_year_days_in_year
            intermediate_years_fraction = end_year - start_year - 1

            return start_year_fraction + end_year_fraction + intermediate_years_fraction


def get_day_count_convention(name: str, start_date: date, end_date: date) -> DayCountConvention:
    conventions = {
        'Actual/360': Actual360,
        'Actual/365': Actual365,
        'Actual/Actual': ActualActual
    }
    if name not in conventions:
        raise ValueError(f"Unknown day count convention: {name}")
    return conventions[name](start_date, end_date)
