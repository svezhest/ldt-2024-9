from pydantic import BaseModel, ConfigDict

from api_v1.workload.workload import WorkloadType


class Skills(BaseModel):
    primary_skill: WorkloadType
    secondary_skills: list[WorkloadType]
