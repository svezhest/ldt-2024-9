
import datetime


def date_to_year_and_week_number(date: datetime.date) -> tuple[int, int]:
    return [date.year, int(date.strftime("%W"))]
