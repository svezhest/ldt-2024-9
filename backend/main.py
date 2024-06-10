from calendar import monthrange
import datetime
from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body

from mytypes.schedule import DaySchedule, Interval, Schedule, WorkStatus
from mytypes.workload import WorkDayResults, WorkResult, Workload, WorkloadEntry, WorkloadType, parse_workload_type

app = FastAPI()


# =====
# ПРОГНОЗЫ
# =====

@app.get("/workload/{workload_type}")
async def get_workload(workload_type: str, year: Optional[int] = None, week_number: Optional[int] = None) -> list[Workload]:
    '''
    Отдаёт данные по количеству исследований, фактические и прогнозные.
    year и week_number выступают как фильтры.
    '''
    return [
        Workload(amount=100, workload_type=parse_workload_type(
            workload_type), year=2024, week_number=1),
        Workload(amount=1000, workload_type=WorkloadType.RG,
                 year=2024, week_number=2),
    ]


@app.post("/workload/{workload_type}")
async def post_workload(workload_type: str,  value: WorkloadEntry = Body()):
    '''
    Позволяет внести новые фактические данные по исследованиям за определенную неделю.
    '''
    pass

# =====
# ГРАФИК, ОТЧЕТЫ
# =====


@app.post("/reports/{doctor_id}")
async def post_report(doctor_id: int,  value: WorkDayResults = Body()):
    '''
    Отправить результаты за день
    '''
    pass


@app.get("/reports/{doctor_id}")
async def get_week_report(doctor_id: int) -> list[WorkDayResults]:
    '''
    Получить результаты за текущую неделю
    '''
    return [
        WorkDayResults(date=datetime.date(2024, 6, 3), results_by_type=[
                       WorkResult(amount=100, workload_type=WorkloadType.CT)]),
        WorkDayResults(date=datetime.date(2024, 6, 4), results_by_type=[
                       WorkResult(amount=300, workload_type=WorkloadType.CT)]),
        WorkDayResults(date=datetime.date(2024, 6, 5), results_by_type=[
                       WorkResult(amount=200, workload_type=WorkloadType.CT)]),
        WorkDayResults(date=datetime.date(2024, 6, 6), results_by_type=[WorkResult(
            amount=100, workload_type=WorkloadType.CT), WorkResult(amount=15, workload_type=WorkloadType.CT_CONTRAST)]),
        WorkDayResults(date=datetime.date(2024, 6, 7), results_by_type=[
                       WorkResult(amount=100, workload_type=WorkloadType.CT)]),
        WorkDayResults(date=datetime.date(2024, 6, 8), results_by_type=[]),
        WorkDayResults(date=datetime.date(2024, 6, 9), results_by_type=[]),
    ]


@app.put("/schedule/{doctor_id}")
async def edit_schedule(doctor_id: int,  value: Schedule = Body()):
    '''
    Изменить расписание врачу.
    Данные вводятся в реальных датах, заполняется одна или две недели. Внутри расписание применяется ко всему времени работы.
    '''
    pass


@app.get("/schedule/default")
async def get_default_schedule(rate: float = 1.0) -> Schedule:
    today = datetime.date.today()
    first_month_day = today + datetime.timedelta(days=-today.day)
    days_in_month = monthrange(today.year, today.month)[1]
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
                end_time=(datetime.datetime.combine(datetime.date(1,1,1), start_time) + datetime.timedelta(hours=work_hours)).time(),
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
        doctor_id=0,
        schedule=schedule
    )


@app.get("/schedule/{doctor_id}")
async def get_schedule(doctor_id: int, from_date: datetime.date, to_date: datetime.date) -> Schedule:
    return Schedule(doctor_id=doctor_id, schedule=[])
