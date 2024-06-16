import datetime
from pydantic import BaseModel

from api_v1.workload.workload import WorkloadType


class Report(BaseModel):
    doctor_id: int
    date: datetime.date
    workload_type: WorkloadType
    amount: int
