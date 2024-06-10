from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from enum import Enum

app = FastAPI()


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
