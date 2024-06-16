from pydantic import BaseModel

from api_v1.workload.workload import WorkloadType
from logic.schemas import RecommendationType


class WorkloadTypeStats(BaseModel):
    workload_type: WorkloadType
    done: int
    done_prediction: int
    needed_prediction: int
    recommendation: RecommendationType


class Stats(BaseModel):
    stats: list[WorkloadTypeStats]
