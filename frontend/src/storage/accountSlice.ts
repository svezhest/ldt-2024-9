import {createSlice, PayloadAction} from '@reduxjs/toolkit'
// by_sheer_willpower
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

interface AccountState {
  startHours?: '08:00' | '09:00' | '14:00' | '20:00'
  shiftingType?: '5/2' | '2/2'
  hoursPerWeel?: 40 | 20 | 30
  fullName?: string
  dateOfBirth?: string
  position?: string
  specialization?: string
  phoneNumber?: string
  email?: string
  skills?: {
    primary_skill: WorkloadType
    secondary_skills: WorkloadType[]
  }
  role?: 'admin' | 'hr' | 'analyst' | 'doctor'
  token?: string
}

const initialState: AccountState = {
  startHours: undefined,
  shiftingType: undefined,
  hoursPerWeel: undefined,
  fullName: undefined,
  dateOfBirth: undefined,
  position: undefined,
  specialization: undefined,
  phoneNumber: undefined,
  email: undefined,
  skills: undefined,
  role: undefined,
  token: undefined,
}

const chatWithSlice = createSlice({
  name: 'account',
  initialState,
  reducers: {
    setAccountData(state, action: PayloadAction<AccountState>) {
      state.startHours = action.payload.startHours
      state.shiftingType = action.payload.shiftingType
      state.hoursPerWeel = action.payload.hoursPerWeel
      state.fullName = action.payload.fullName
      state.dateOfBirth = action.payload.dateOfBirth
      state.position = action.payload.position
      state.specialization = action.payload.specialization
      state.phoneNumber = action.payload.phoneNumber
      state.email = action.payload.email
      state.skills = action.payload.skills
      state.role = action.payload.role
      state.token = action.payload.token
    },
    clearAccountData(state) {
      ;(state.startHours = undefined),
        (state.shiftingType = undefined),
        (state.hoursPerWeel = undefined),
        (state.fullName = undefined),
        (state.dateOfBirth = undefined),
        (state.position = undefined),
        (state.specialization = undefined),
        (state.phoneNumber = undefined),
        (state.email = undefined),
        (state.skills = undefined),
        (state.role = undefined),
        (state.token = undefined)
    },
  },
})

export const {setAccountData, clearAccountData} = chatWithSlice.actions
export default chatWithSlice.reducer
