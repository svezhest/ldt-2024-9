from enum import Enum


class RecommendationType(str, Enum):
    NOTHING = 'nothing'
    CALL_OVERTIME = 'call_overtime'
    STOP_VACATION = 'stop_vacation'
    HIRE = 'hire'
