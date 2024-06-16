from api_v1.workload.workload import WorkloadType


dummy = {
    WorkloadType.DENSITOMETER: 1329,
    WorkloadType.CT: 4882,
    WorkloadType.CT_CONTRAST: 544,
    WorkloadType.CT_CONTRAST_MULTI: 612,
    WorkloadType.MMG: 14002,
    WorkloadType.MRI: 1957,
    WorkloadType.MRI_CONTRAST: 792,
    WorkloadType.MRI_CONTRAST_MULTI: 8,
    WorkloadType.RG: 57966,
    WorkloadType.FLUOROGRAPHY: 18959,

}


def predict(year: int, week_number: int) -> dict[WorkloadType, int]:
    return dummy
