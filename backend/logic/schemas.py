from enum import Enum
from api_v1.doctors.schemas import DoctorConfidentInfo
from api_v1.schedule.schemas import ScheduleEvent
from api_v1.workload.workload import WorkloadType


class RecommendationType(str, Enum):
    NOTHING = 'nothing'
    CALL_OVERTIME = 'call_overtime'
    STOP_VACATION = 'stop_vacation'


class Recommendation:
    doctor_id: int
    recommendation: RecommendationType


def reconsider_schedule(
        doctors: list[DoctorConfidentInfo],
        current_progress: dict[WorkloadType, int],
        predictions_this_week: dict[WorkloadType, int],
        events: list[ScheduleEvent]) -> tuple[list[Recommendation], dict[WorkloadType, int]]:
    '''
    events -- все известные события

    нужен алгоритм расчёта 2/2 (очень скоро сделаю)

    отдаёт рекомендации по известным, если невозможно, в dict[WorkloadType, int]
    будет указано, сколько врачей нанять.
    '''
    pass
