import numpy as np
from typing import List, Dict, Tuple
import datetime
from enum import Enum
from api_v1.doctors.schemas import DoctorConfidentInfo
from api_v1.schedule.schemas import ScheduleEvent
from api_v1.workload.workload import WorkloadType, WorkloadTypeDoctor, workload_mapping
from logic.schemas import RecommendationType


def reconsider_schedule(
        doctors: list[DoctorConfidentInfo],
        current_progress: dict[WorkloadType, int],
        predictions_this_week: dict[WorkloadType, int],
        events: list[ScheduleEvent]) -> dict[WorkloadTypeDoctor, dict[RecommendationType, int]]:
    cur_date = datetime.date.today()
    cap_per_week = 40

    # Определение доступных врачей
    avail_doctors = {wl: [] for wl in WorkloadTypeDoctor}
    for doc in doctors:
        if any(evt.start <= cur_date <= evt.end for evt in events if evt.doc == doc):
            continue
        avail_doctors[doc.primary_skill].append(doc)
        for add_mod in doc.secondary_skills:
            avail_doctors[add_mod].append(doc)

    # Определение требуемых врачей
    req_doctors = {wl: max(0, np.ceil((predictions_this_week.get(
        wl, 0) - current_progress.get(wl, 0)) / cap_per_week)) for wl in WorkloadType}

    # Инициализация рекомендаций
    recs = {wl: {rec: 0 for rec in RecommendationType}
            for wl in WorkloadTypeDoctor}

    # Расчет рекомендаций
    for wl, needed in req_doctors.items():
        if wl in workload_mapping:
            doctor_wl = next(
                (doc_wl for doc_wl, wl_list in workload_mapping.items() if wl in wl_list), None)
            if doctor_wl:
                available_hours = sum(
                    doc.hours_per_week for doc in avail_doctors[doctor_wl])

                if available_hours < needed * cap_per_week:
                    shortfall_hours = needed * cap_per_week - available_hours

                    # Первая приоритет: Вызов на сверхурочные
                    overtime_hours = sum(
                        40 - doc.hours_per_week for doc in avail_doctors[doctor_wl] if doc.hours_per_week < 40)
                    if overtime_hours >= shortfall_hours:
                        recs[doctor_wl][RecommendationType.CALL_OVERTIME] += int(
                            np.ceil(shortfall_hours / 40))
                    else:
                        shortfall_hours -= overtime_hours
                        recs[doctor_wl][RecommendationType.CALL_OVERTIME] += int(
                            np.ceil(overtime_hours / 40))
                        # Вторая приоритет: Прекращение отпуска
                        vacation_hours = sum(doc.hours_per_week for doc in doctors if any(
                            evt.doc == doc and evt.evt_type == 'vac' for evt in evts) and doc.primary_skill == doctor_wl)
                        if vacation_hours >= shortfall_hours:
                            recs[doctor_wl][RecommendationType.STOP_VACATION] += int(
                                np.ceil(shortfall_hours / 40))
                        else:
                            shortfall_hours -= vacation_hours
                            recs[doctor_wl][RecommendationType.STOP_VACATION] += int(
                                np.ceil(vacation_hours / 40))

                            # Третья приоритет: Нанять новых врачей
                            recs[doctor_wl][RecommendationType.HIRE] += int(
                                np.ceil(shortfall_hours / 40))
                else:
                    recs[doctor_wl][RecommendationType.NOTHING] += 1

    return recs
