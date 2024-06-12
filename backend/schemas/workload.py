import datetime
from enum import Enum

from pydantic import BaseModel


class WorkloadType(str, Enum):
    DENSITOMETER = 'densitometer'
    CT = 'ct'
    CT_CONTRAST = 'ct_contrast'
    CT_CONTRAST_MULTI = 'ct_contrast_multi'
    MMG = 'mmg'
    MRI = 'mri'
    MRI_CONTRAST = 'mri_contrast'
    MRI_CONTRAST_MULTI = 'mri_contrast_multi'
    RG = 'rg'
    FLUOROGRAPHY = 'fluorography'


def parse_workload_type(workload_type: str):
    workload_type = workload_type.upper().strip()
    return WorkloadType[workload_type]


class WorkloadEntry(BaseModel):
    amount: int
    year: int
    week_number: int


class Workload(WorkloadEntry):
    workload_type: WorkloadType
    is_predicted: bool


class WorkResult(BaseModel):
    amount: int
    workload_type: WorkloadType


class WorkDayResults(BaseModel):
    results_by_type: list[WorkResult]
    date: datetime.date
