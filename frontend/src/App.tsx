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
} from './pages'
import {Route, Routes} from 'react-router-dom'

export const App = () => {
  useEffect(() => {
    // eslint-disable-next-line no-console
    console.log('render')
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
