import React, {useEffect} from 'react'
import {
  AuthFirst,
  AuthSecond,
  Main,
  Calendar,
  Profile,
  Job,
  Detect,
  Doctors,
  Absence,
  Settings,
  AddAbsence,
  AddDoctor,
} from './pages'
import {Route, Routes} from 'react-router-dom'
import {getCookie} from './tools/getJWT'
import {getMyself} from './api'
import {setAccountData} from './storage/accountSlice'
import {AppDispatch} from './storage/store'
import {useDispatch} from 'react-redux'

export const App = () => {
  const dispatch = useDispatch<AppDispatch>()

  // const handleLogout = () => {
  //   document.cookie = 'jwtToken=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;'
  //   setToken(null)
  // }

  useEffect(() => {
    const storedToken = getCookie('jwtToken')
    if (storedToken) {
      const {token, expiry} = JSON.parse(storedToken)

      const expiryDate = new Date(expiry)
      const currentDate = new Date()

      if (expiryDate.getTime() < currentDate.getTime()) {
        document.cookie = 'jwtToken=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;'
        return
      }

      getMyself(token)
        .then((res) => {
          dispatch(
            setAccountData({
              id: res.id,
              fullName: res.full_name,
              dateOfBirth: res.date_of_birth,
              position: res.position,
              specialization: res.specialization,
              token: token,
            })
          )
        })
        .then(() => {
          // changeAccountStatus(1, 'ok', token)
        })
    }
  }, [])

  return (
    <Routes>
      <Route path='/' element={<AuthFirst />} />
      <Route path='/auth' element={<AuthSecond profile='doctor' />} />
      <Route path='/auth/doctor' element={<AuthSecond profile='doctor' />} />
      <Route path='/auth/Head' element={<AuthSecond profile='head' />} />
      <Route path='/auth/HR' element={<AuthSecond profile='HR' />} />
      <Route
        path='/profile'
        element={
          <Main>
            <Profile />
          </Main>
        }
      />
      <Route
        path='/calendar'
        element={
          <Main>
            <Calendar />
          </Main>
        }
      />
      <Route
        path='/job'
        element={
          <Main>
            <Job />
          </Main>
        }
      />
      <Route
        path='/detect'
        element={
          <Main>
            <Detect />
          </Main>
        }
      />
      <Route
        path='/doctors'
        element={
          <Main>
            <Doctors />
          </Main>
        }
      />
      <Route
        path='/add_doctors'
        element={
          <Main>
            <AddDoctor />
          </Main>
        }
      />
      <Route
        path='/absence'
        element={
          <Main>
            <Absence />
          </Main>
        }
      />
      <Route
        path='/absence/add'
        element={
          <Main>
            <AddAbsence />
          </Main>
        }
      />
      <Route
        path='/settings'
        element={
          <Main>
            <Settings />
          </Main>
        }
      />
    </Routes>
  )
}
