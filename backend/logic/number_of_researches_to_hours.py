from api_v1.workload.workload import WorkloadType

mapping = {
    WorkloadType.DENSITOMETER: 2.2,
    WorkloadType.CT: 11.6,
    WorkloadType.CT_CONTRAST: 18.8,
    WorkloadType.CT_CONTRAST_MULTI: 26.6,
    WorkloadType.MMG: 3.7,
    WorkloadType.MRI: 15.1,
    WorkloadType.MRI_CONTRAST: 19.7,
    WorkloadType.MRI_CONTRAST_MULTI:  30.1,
    WorkloadType.RG: 3.7,
    WorkloadType.FLUOROGRAPHY: 1.0,
}

researches_per_shift_minimum = 181.0
shift_duration = 8

researches_per_hour_minimum = researches_per_shift_minimum / shift_duration


def number_of_researches_to_hours(workload_type: WorkloadType, amount: int) -> float:
    return mapping[workload_type] * amount / researches_per_hour_minimum


def hours_to_number_of_researches(workload_type: WorkloadType, hours: float) -> int:
    return int(hours * researches_per_hour_minimum / mapping[workload_type])
