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


class WorkloadTypeDoctor(str, Enum):
    CT = 'ct'
    MMG = 'mmg'
    MRI = 'mri'
    RG = 'rg'


workload_mapping = {
    WorkloadTypeDoctor.CT: [
        WorkloadType.CT,
        WorkloadType.CT_CONTRAST,
        WorkloadType.CT_CONTRAST_MULTI,
    ],
    WorkloadTypeDoctor.MMG: [
        WorkloadType.MMG
    ],
    WorkloadTypeDoctor.MRI: [
        WorkloadType.MRI,
        WorkloadType.MRI_CONTRAST,
        WorkloadType.MRI_CONTRAST_MULTI,
    ],
    WorkloadTypeDoctor.RG: [
        WorkloadType.RG,
        WorkloadType.FLUOROGRAPHY,
        WorkloadType.DENSITOMETER
    ]
}


proportions = {
    WorkloadTypeDoctor.CT: [
        (WorkloadType.CT, 0.673297538766856),
        (WorkloadType.CT_CONTRAST, 0.126725211211868),
        (WorkloadType.CT_CONTRAST_MULTI, 0.199977250021277),
    ],
    WorkloadTypeDoctor.MMG: [
        (WorkloadType.MMG, 1),
    ],
    WorkloadTypeDoctor.MRI: [
        (WorkloadType.MRI, 0.654877831369728),
        (WorkloadType.MRI_CONTRAST, 0.339483895807981),
        (WorkloadType.MRI_CONTRAST_MULTI, 0.00563827282229106),
    ],
    WorkloadTypeDoctor.RG: [
        (WorkloadType.RG, 0.905777992975203),
        (WorkloadType.FLUOROGRAPHY, 0.082222743823554),
        (WorkloadType.DENSITOMETER, 0.0119992632012432),
    ],
}


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
