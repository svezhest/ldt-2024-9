import datetime
from urllib.request import urlopen


def save_production_calendar(year):
    response = urlopen(
        f'https://isdayoff.ru/api/getdata?year={year}', timeout=2).read()

    with open(f'dayoffs_{year}.txt', 'w') as f:
        f.write(response.decode())


def parse_production_calendar(year: int) -> dict[str, bool]:
    date = datetime.date(year=year, month=1, day=1)

    result = {}

    with open(f'dayoffs_{year}.txt') as f:
        for ch in f.read():
            result[str(date)] = bool(int(ch))
            date += datetime.timedelta(days=1)

        return result
