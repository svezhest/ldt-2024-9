// AccountStatus.ts
export type AccountStatus = 'new' | 'ok' | 'deleted'

// Token.ts
export interface Token {
  access_token: string
  token_type: string
}

// ValidationError.ts
export interface ValidationError {
  loc: (string | number)[]
  msg: string
  type: string
}

// Doctor.ts
export interface Doctor {
  start_hours: StartHours
  shifting_type: ShiftingType
  hours_per_weel: HoursPerWeek
  full_name: string
  date_of_birth: string // date
  position: string
  specialization: string
  phone_number: string
  email: string
  skills: Skills
  role: Role
  password: string
  account_status?: AccountStatus // default: new
  id: number
}

// DoctorConfidentInfo.ts
export interface DoctorConfidentInfo {
  start_hours: StartHours
  shifting_type: ShiftingType
  hours_per_weel: HoursPerWeek
  full_name: string
  date_of_birth: string // date
  position: string
  specialization: string
  phone_number: string
  email: string
  skills: Skills
  role: Role
}

// DoctorPartial.ts
export interface DoctorPartial {
  start_hours?: StartHours
  shifting_type?: ShiftingType
  hours_per_weel?: HoursPerWeek
  full_name?: string | null
  date_of_birth?: string | null // date
  position?: string | null
  specialization?: string | null
  phone_number?: string | null
  email?: string | null
  skills?: Skills | null
  role?: Role | null
  password?: string
  account_status?: AccountStatus // default: new
}

// DoctorPublicInfo.ts
export interface DoctorPublicInfo {
  full_name: string
  date_of_birth: string // date
  position: string
  specialization: string
}

// DoctorTechnicalInfo.ts
export interface DoctorTechnicalInfo {
  start_hours: StartHours
  shifting_type: ShiftingType
  hours_per_week: HoursPerWeek
  full_name: string
  date_of_birth: string // date
  position: string
  specialization: string
  phone_number: string
  email: string
  skills: Skills
  role: Role
  password: string
  account_status?: AccountStatus // default: new
}

// Other necessary types
export type HoursPerWeek = 20 | 30 | 40
export type Role = 'admin' | 'hr' | 'analyst' | 'doctor'
export type ShiftingType = '5/2' | '2/2'
export type StartHours = '08:00' | '09:00' | '14:00' | '20:00'

export interface Skills {
  primary_skill: WorkloadType
  secondary_skills: WorkloadType[]
}

export type WorkloadType =
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

export type GetStats = {
  stats: {
    workload_type: WorkloadType
    done: number
    done_prediction: number
    needed_prediction: number
    recommendation: 'nothing' | 'call_overtime' | 'stop_vacation' | 'hire'
  }[]
}
