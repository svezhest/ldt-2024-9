import {createSlice, PayloadAction} from '@reduxjs/toolkit'

interface AccountState {
  id?: number
  fullName?: string
  dateOfBirth?: string
  position?: string
  specialization?: string
  token?: string
}

const initialState: AccountState = {
  id: undefined,
  fullName: undefined,
  dateOfBirth: undefined,
  position: undefined,
  specialization: undefined,
  token: undefined,
}

const chatWithSlice = createSlice({
  name: 'account',
  initialState,
  reducers: {
    setAccountData(state, action: PayloadAction<AccountState>) {
      state.id = action.payload.id
      state.fullName = action.payload.fullName
      state.position = action.payload.position
      state.specialization = action.payload.specialization
      state.token = action.payload.token
      state.dateOfBirth = action.payload.dateOfBirth
    },
    clearAccountData(state) {
      ;(state.fullName = undefined),
        (state.id = undefined),
        (state.dateOfBirth = undefined),
        (state.position = undefined),
        (state.specialization = undefined),
        (state.token = undefined)
    },
  },
})

export const {setAccountData, clearAccountData} = chatWithSlice.actions
export default chatWithSlice.reducer
