import datetime

from api_v1.schedule.schemas import DaySchedule, Interval, Schedule, StartHours
from core.models.doctor import Doctor
from pathlib import Path
import json

from logic.date_decomposition import date_to_year_and_week_number
from logic.production_calendar import parse_production_calendar, save_production_calendar

dayoffs = None
network_failed = False


def is_day_off(date: datetime.date):
    global dayoffs
    global network_failed

    year = date.year

    if dayoffs is not None and dayoffs[1] == year:
        return dayoffs[0][str(date)]
    if Path(f'dayoffs_{year}.txt').exists():
        dayoffs = (parse_production_calendar(year), year)
    elif not network_failed:
        try:
            save_production_calendar(year)
            dayoffs = (parse_production_calendar(year), year)
        except:
            network_failed = True
    return date.weekday() > 4


def add_hours(start: datetime.time, hours_delta: float) -> datetime.time:
    return (datetime.datetime.combine(datetime.date(
        1, 1, 1), start) + datetime.timedelta(hours=hours_delta)).time()


def generate_schedule(starting_hours: StartHours, duration: int):
    if duration >= 11:
        break_time = 1.
    else:
        break_time = 0.5

    first_half = duration // 2

    if starting_hours == '08:00':
        starting_hours = datetime.time(hour=8)
    elif starting_hours == '09:00':
        starting_hours = datetime.time(hour=9)
    elif starting_hours == '14:00':
        starting_hours = datetime.time(hour=14)
    elif starting_hours == '20:00':
        starting_hours = datetime.time(hour=20)

    return DaySchedule(
        intervals=[
            Interval(
                start_time=starting_hours,
                end_time=add_hours(starting_hours, first_half),
                is_break=False
            ),
            Interval(
                start_time=add_hours(starting_hours, first_half),
                end_time=add_hours(starting_hours, first_half + break_time),
                is_break=True
            ),
            Interval(
                start_time=add_hours(starting_hours, first_half + break_time),
                end_time=add_hours(starting_hours, duration + break_time),
                is_break=False
            ),
        ],
        date=datetime.date.today(),
        total_working_time=datetime.time(hour=duration, minute=0, second=0),
        total_break_time=datetime.time(
            hour=0 if break_time == 0.5 else 1, minute=30 if break_time == 0.5 else 0, second=0)
    )


def calculate_schedule(
    date_from: datetime.date,
    date_to: datetime.date,
    doctor: Doctor
) -> Schedule:
    # 12 * 6 = 72, 12 * 7 = 84
    # 11 * 4 + 12 * 3 = 44 + 36 = 80
    # 2/2 (80, 2w): 01 02 03 04 05 06 07 08 09 10 11 12 13 14
    #               11 -- 12 11 -- -- 12 -- 11 -- -- 12 11 --

    # 12 * 5 = 60
    # 2/2 (60, 2w): 01 02 03 04 05 06 07 08 09 10 11 12 13 14
    #               12 -- -- 12 -- -- 12 -- 12 -- -- 12 -- --

    # 12 * 3 = 36, 12 * 4 = 48 -- тут не получится
    # 2/2 (80, 4w): 01 02 03 04 05 06 07 08 09 10 11 12 13 14 01 02 03 04 05 06 07 08 09 10 11 12 13 14
    #               -- 11 -- -- -- 12 -- -- 11 -- -- -- -- 12 -- -- -- 11 -- -- -- 12 -- -- -- 11 -- --

    res = []

    if doctor.shifting_type == '5/2':
        if doctor.hours_per_week == 20:
            current_date = date_from + \
                datetime.timedelta(days=-date_from.weekday())
            _, week = date_to_year_and_week_number(current_date)
            assigned = 0
            while current_date <= date_to:
                if not is_day_off(current_date) and current_date >= date_from and assigned < 3:
                    day_schedule = generate_schedule(doctor.start_hours,
                                                     7 if assigned < 2 else 6)
                    day_schedule.date = current_date
                    res.append(day_schedule)
                    assigned += 1

                current_date += datetime.timedelta(days=1)
                _, current_week = date_to_year_and_week_number(current_date)
                if week != current_week:
                    assigned = 0
                    week = current_week
        else:
            current_date = date_from
            while current_date <= date_to:
                if not is_day_off(current_date):
                    day_schedule = generate_schedule(doctor.start_hours,
                                                     6 if doctor.hours_per_week == 30 else 8)
                    day_schedule.date = current_date
                    res.append(day_schedule)
                current_date += datetime.timedelta(days=1)
    else:
        first_month_day = date_from + datetime.timedelta(days=-date_from.day)
        current_date = first_month_day + \
            datetime.timedelta(days=-first_month_day.weekday)

        if doctor.hours_per_week == 20:
            schedule_4_weeks = [
                0, 11, 0, 0, 0, 12, 0, 0, 11, 0, 0, 0, 0, 12, 0, 0, 0, 11, 0, 0, 0, 12, 0, 0, 0, 11, 0, 0
            ]
        elif doctor.hours_per_week == 30:
            schedule_4_weeks = [
                12, 0, 0, 12, 0, 0, 12, 0, 12, 0, 0, 12, 0, 0, 12, 0, 0, 12, 0, 0, 12, 0, 12, 0, 0, 12, 0, 0
            ]
        elif doctor.hours_per_week == 40:
            schedule_4_weeks = [
                11, 0, 12, 11, 0, 0, 12, 0, 11, 0, 0, 12, 11, 0, 11, 0, 12, 11, 0, 0, 12, 0, 11, 0, 0, 12, 11, 0
            ]

        idx = 0
        while current_date <= date_to:
            if current_date >= date_from:
                if schedule_4_weeks[idx] == 0:
                    day_schedule = DaySchedule(
                        intervals=[],
                        date=current_date,
                        total_break_time=0,
                        total_working_time=0
                    )
                else:
                    day_schedule = generate_schedule(
                        doctor.start_hours,
                        schedule_4_weeks[idx])
                    day_schedule.date = current_date
                res.append(day_schedule)
            current_date += datetime.timedelta(days=1)
            idx = (idx + 1) % 28

    return Schedule(
        schedule=res
    )
