import datetime
from api_v1.schedule.schemas import Events, Schedule
from core.models.doctor import Doctor
from api_v1.workload.workload import workload_mapping
from logic.calculate_schedule import calculate_schedule
from .predict import mapping, mapping_back
import pandas as pd


def format_schedule(doctor: Doctor, schedule: Schedule, start_date: datetime.date, events: Events) -> dict:
    if start_date.day != 1:
        start_date += datetime.timedelta(days=-start_date.day + 1)

    first_skill = mapping_back[doctor.skills.primary_skill]
    rest_skills = '' if len(doctor.skills.secondary_skills) == 0 else ', '.join([mapping_back[workload_type]
                                                                                 for workload_doctor_type in doctor.skills.secondary_skills for workload_type in workload_mapping[workload_doctor_type]])

    res = []

    period_titles = ['с', 'до', 'перерыв', 'отраб.']

    total = 0

    for idx in range(4):
        date = start_date
        current_month = date.month
        schedule_idx = 0
        day_schedule = None
        if idx == 2:
            temp = {
                'Фамилия, Имя, Отчество': doctor.full_name,
                'Модальность': first_skill,
                'Дополнительные модальности': rest_skills,
                'Ставка': doctor.hours_per_week / 40,
                'Таб.№': doctor.id,
                '-': period_titles[idx],
            }
        else:
            temp = {
                'Фамилия, Имя, Отчество': '',
                'Модальность': '',
                'Дополнительные модальности': '',
                'Ставка': '',
                'Таб.№': '',
                '-': period_titles[idx],
            }

        day = 1
        inserted_half = False
        while date.month == current_month:
            if day == 15 and not inserted_half:
                inserted_half = True
                if idx == 3:
                    temp['Итого за 1 пол. месяца'] = total
                else:
                    temp['Итого за 1 пол. месяца'] = ''
                continue

            if schedule_idx > len(schedule.schedule) or schedule.schedule[schedule_idx].date != date:
                day_schedule = None
            else:
                day_schedule = schedule.schedule[schedule_idx]
                schedule_idx += 1

            if idx == 0:
                temp[day] = '' if day_schedule is None or len(
                    day_schedule.intervals) == 0 else str(day_schedule.intervals[0].start_time)
            elif idx == 1:
                temp[day] = '' if day_schedule is None or len(
                    day_schedule.intervals) == 0 else str(day_schedule.intervals[-1].end_time)
            elif idx == 2:
                temp[day] = '' if day_schedule is None else day_schedule.total_break_time.minute + \
                    day_schedule.total_break_time.hour * 60
            else:
                total += (0 if day_schedule is None else day_schedule.total_working_time.hour)
                temp[day] = '' if day_schedule is None else day_schedule.total_working_time.hour

            day += 1
            date += datetime.timedelta(days=1)

        if idx == 3:
            temp['Итого за 2 пол. месяца'] = total
            temp['Норма часов по графику'] = doctor.hours_per_week * 4
            temp['Норма часов за полный месяц'] = doctor.hours_per_week * 4
            temp['Дата'] = ''
        else:
            temp['Итого за 2 пол. месяца'] = ''
            temp['Норма часов по графику'] = ''
            temp['Норма часов за полный месяц'] = ''
            temp['Дата'] = ''
        res.append(temp)
    return res


def generate_doctor_table(doctors: list[Doctor], date: datetime.date, events: Events):
    res = []

    start_date = date + datetime.timedelta(days=-date.day + 1)
    end_time = start_date + datetime.timedelta(days=31)

    for doctor in doctors:
        schedule = calculate_schedule(
            date_from=start_date, date_to=end_time, doctor=doctor)
        res.extend(format_schedule(doctor, schedule, start_date, events))

    df = pd.DataFrame(res)
    df.to_excel('table.xlsx')
