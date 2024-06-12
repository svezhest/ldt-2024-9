from pydantic import BaseModel, ConfigDict
from schemas.workload import WorkloadType


class Skills(BaseModel):
    primary_skill: WorkloadType
    secondary_skills: list[WorkloadType]
