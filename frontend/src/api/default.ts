import axios from 'axios'

const api = axios.create({
  baseURL: 'http://your-api-base-url.com',
})

// Types
type WorkloadType =
  | 'densitometer'
  | 'ct'
  | 'ct_contrast'
  | 'ct_contrast_multi'
  | 'mmg'
  | 'mri'
  | 'mri_contrast'
  | 'mri_contrast_multi'
  | 'rg'
  | 'fluorography'

type Workload = {
  amount: number
  year: number
  week_number: number
  workload_type: WorkloadType
  is_predicted: boolean
}

type WorkloadEntry = {
  amount: number
  year: number
  week_number: number
}

type WorkDayResultsInput = {
  results_by_type: WorkResult[]
  date: string
}

type WorkResult = {
  amount: number
  workload_type: WorkloadType
}

type DayScheduleInput = {
  intervals: Interval[]
  date: string
  total_break_time: string
  total_working_time: string
}

type Interval = {
  start_time: string
  end_time: string
  status: WorkStatus
}

type WorkStatus = 'working' | 'break' | 'home' | 'vacation' | 'force_majeure'

type ScheduleInput = {
  doctor_id: number
  schedule: DayScheduleInput[]
}

type DoctorInfo = {
  id: number
  full_name: string
  date_of_birth: string
  phone_number: string
  email: string
  position: string
  skills: Skills
}

type Skills = {
  primary_skill: WorkloadType
  secondary_skills: WorkloadType[]
}

// API functions
// Workload
export const getWorkload = async (
  workload_type: WorkloadType,
  year?: number,
  week_number?: number
): Promise<Workload[]> => {
  const params = {year, week_number}
  const response = await api.get<Workload[]>(`/workload/${workload_type}`, {params})
  return response.data
}

export const postWorkload = async (workload_type: WorkloadType, entry: WorkloadEntry): Promise<void> => {
  await api.post(`/workload/${workload_type}`, entry)
}

// Reports
export const postReport = async (doctor_id: number, report: WorkDayResultsInput): Promise<void> => {
  await api.post(`/reports/${doctor_id}`, report)
}

export const getWeekReport = async (doctor_id: number): Promise<WorkDayResultsInput[]> => {
  const response = await api.get<WorkDayResultsInput[]>(`/reports/${doctor_id}`)
  return response.data
}

// Schedule
export const getSchedule = async (doctor_id: number, from_date: string, to_date: string): Promise<ScheduleInput> => {
  const params = {from_date, to_date}
  const response = await api.get<ScheduleInput>(`/schedule/${doctor_id}`, {params})
  return response.data
}

export const editSchedule = async (doctor_id: number, schedule: ScheduleInput): Promise<void> => {
  await api.put(`/schedule/${doctor_id}`, schedule)
}

export const getDefaultSchedule = async (rate: number = 1.0): Promise<ScheduleInput> => {
  const params = {rate}
  const response = await api.get<ScheduleInput>('/schedule/default', {params})
  return response.data
}

// Doctor
export const getDoctor = async (doctor_id: number): Promise<DoctorInfo> => {
  const response = await api.get<DoctorInfo>(`/doctors/${doctor_id}`)
  return response.data
}
