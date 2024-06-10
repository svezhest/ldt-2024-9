from enum import Enum

from pydantic import BaseModel


class WorkloadType(Enum):
    DENSITOMETER = 1
    CT = 2
    CT_CONTRAST = 3
    CT_CONTRAST_MULTI = 4
    MMG = 5
    MRI = 6
    MRI_CONTRAST = 7
    MRI_CONTRAST_MULTI = 8
    RG = 9
    FLUOROGRAPHY = 10


class WorkloadEntry(BaseModel):
    amount: int
    year: int
    week_number: int


class Workload(WorkloadEntry):
    workload_type: WorkloadType
    is_predicted: bool


def parse_workload_type(workload_type: str):
    workload_type = workload_type.upper().strip()
    return WorkloadType[workload_type]
