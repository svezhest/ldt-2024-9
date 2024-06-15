from calendar import monthrange
import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.schedule.schemas import DaySchedule, Interval, Schedule, WorkStatus
from core.models.schedule import Schedule as ScheduleDB
from core.models.schedule import DaySchedule as DayScheduleDB
from core.models.schedule import Interval as IntervalDB

def get_default_schedule(month_date: datetime.date, rate: float = 1.0) -> Schedule:
    first_month_day = month_date + datetime.timedelta(days=-month_date.day)
    days_in_month = monthrange(month_date.year, month_date.month)[1]
    if days_in_month > 28:
        working_days = [1, 4, 6, 7, 11, 13, 15, 18, 20, 22, 25, 27, 29]
    else:
        working_days = [1, 4, 6, 7, 9, 11, 13, 15, 18, 20, 22, 25, 27]
    relaxed_day = 7

    schedule = []

    for day in range(1, days_in_month + 1):
        if day not in working_days:
            continue

        base_hours = 12
        if day == relaxed_day:
            base_hours = 11

        work_hours = base_hours * rate

        intervals = []

        start_time = datetime.time(hour=8)
        break_time = 0

        if work_hours > 4.0:
            intervals.extend([
                Interval(
                    start_time=start_time,
                    end_time=datetime.time(hour=11),
                    status=WorkStatus.WORKING
                ),
                Interval(
                    start_time=datetime.time(hour=11),
                    end_time=datetime.time(hour=11, minute=30),
                    status=WorkStatus.BREAK
                ),
            ])
            start_time = datetime.time(hour=11, minute=30)
            work_hours -= 3
            break_time = 30

        intervals.append(
            Interval(
                start_time=start_time,
                end_time=(datetime.datetime.combine(datetime.date(
                    1, 1, 1), start_time) + datetime.timedelta(hours=work_hours)).time(),
                status=WorkStatus.WORKING
            )
        )
        schedule.append(
            DaySchedule(
                intervals=intervals,
                date=first_month_day + datetime.timedelta(days=day - 1),
                total_break_time=datetime.timedelta(minutes=break_time),
                total_working_time=datetime.timedelta(hours=base_hours * rate)
            )
        )

    return Schedule(
        schedule=schedule
    )


async def create_schedule(schedule: Schedule, session: AsyncSession):
    session_schedule = ScheduleDB()
    session.add(session_schedule)
    await session.commit()
    await session.refresh(session_schedule)
    
    for day_schedule in schedule.day_schedules:
        session_day_schedule = DayScheduleDB(
            date=day_schedule.date,
            total_break_time=day_schedule.total_break_time,
            total_working_time=day_schedule.total_working_time,
            schedule_id=session_schedule.id
        )
        session.add(session_day_schedule)
        await session.commit()
        await session.refresh(session_day_schedule)
        
        for interval in day_schedule.intervals:
            session_interval = IntervalDB(
                start_time=interval.start_time,
                end_time=interval.end_time,
                status=interval.status,
                day_schedule_id=session_day_schedule.id
            )
            session.add(session_interval)
        await session.commit()


async def get_schedule():
    pass
