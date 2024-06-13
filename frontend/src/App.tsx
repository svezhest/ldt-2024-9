import React from 'react'
import {AuthFirst, AuthSecond} from './pages'
import {Route, Routes} from 'react-router-dom'
import {Main} from './pages/Main'
import {Calendar} from './pages/Calendar'
import {Profile} from './pages/Profile'

export const App = () => {
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
    </Routes>
  )
}
