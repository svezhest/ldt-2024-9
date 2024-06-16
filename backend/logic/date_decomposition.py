
import datetime


def date_to_year_and_week_number(date: datetime.date) -> tuple[int, int]:
    return [date.year, int(date.strftime("%W"))]


def year_and_week_number_to_date(year: int, week_number: int) -> datetime.date:
    date = datetime.datetime(year, 1, 1, 0, 0, 0, 0)
    return date + datetime.timedelta(days=(7 * (week_number - 1) - date.weekday()))
