import React from 'react'
import {BlueButton} from '../../ui-kit'
import {createUseStyles} from 'react-jss'
import {Doctor, Head, HR} from './logos'
import {useNavigate} from 'react-router-dom'

export const AuthFirst = () => {
  const c = useStyles()
  const navigate = useNavigate()

  return (
    <div className={c.root}>
      <BlueButton
        text='Руководитель референс-центра'
        onClick={() => {
          navigate('/auth/head')
        }}
      >
        <Head />
      </BlueButton>
      <BlueButton
        text='Врач'
        onClick={() => {
          navigate('/auth/doctor')
        }}
      >
        <Doctor />
      </BlueButton>
      <BlueButton
        text='Кадровый специалист'
        onClick={() => {
          navigate('/auth/HR')
        }}
      >
        <HR />
      </BlueButton>
    </div>
  )
}

const useStyles = createUseStyles({
  root: {
    minHeight: '100vh',
    minWidth: '100vw',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    flexDirection: 'column',
    gap: 15,
  },
})
