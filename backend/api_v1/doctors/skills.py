from pydantic import BaseModel, ConfigDict

from api_v1.workload.workload import WorkloadTypeDoctor


class Skills(BaseModel):
    primary_skill: WorkloadTypeDoctor
    secondary_skills: list[WorkloadTypeDoctor]
