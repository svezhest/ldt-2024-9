from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body

from backend.types.workload import Workload, WorkloadEntry, WorkloadType, parse_workload_type

app = FastAPI()


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
