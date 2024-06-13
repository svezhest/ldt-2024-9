import {BlueButton, ArrowLeft} from '../../ui-kit'
import React from 'react'
import {createUseStyles} from 'react-jss'
import cn from 'classnames'
import {useNavigate} from 'react-router-dom'

type AuthSecondProps = {
  profile: 'doctor' | 'HR' | 'head'
}

export const AuthSecond: React.FC<AuthSecondProps> = () => {
  const c = useStyles()
  const navigate = useNavigate()

  return (
    <div className={c.root}>
      <div className={c.container}>
        <div className={c.header}>
          <button
            onClick={() => {
              navigate('/')
            }}
            className={c.cross}
          >
            <ArrowLeft />
          </button>
          <h2>Вход / Регистрация</h2>
        </div>
        <p className={cn(c.inputHeader, c.margin)}>Email</p>
        <input className={c.input} placeholder='Введите почту' type='email' />
        <p className={c.inputHeader}>Пароль</p>
        <input className={c.input} placeholder='Введите пароль' type='password' />
        <BlueButton className={c.button} text='Войти' size='md' isInverse onClick={() => navigate('/profile')} />
      </div>
    </div>
  )
}

const useStyles = createUseStyles({
  root: {
    height: '100vh',
    width: '100vw',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    flexDirection: 'column',
  },
  container: {
    display: 'flex',
    alignItems: 'flex-start',
    justifyContent: 'center',
    flexDirection: 'column',
    width: 320,
  },
  margin: {
    marginTop: '30px !important',
  },
  button: {
    marginTop: 40,
    width: 320,
  },
  header: {
    display: 'flex',
    fontFamily: 'Inter, sans-serif',
    fontSize: 20,
    fontWeight: 400,
    width: '100%',
    gap: 5,
    justifyContent: 'center',
    alignItems: 'center',
  },
  inputHeader: {
    display: 'flex',
    justifyContent: 'flex-start',
    fontSize: 14,
    fontFamily: 'Inter, sans-serif',
    marginTop: 15,
    paddingLeft: 10,
  },
  input: {
    borderRadius: 12,
    backgroundColor: '#F8F8F8',
    marginTop: 5,
    padding: [15, 20],
    width: 280,

    '&::placeholder': {
      color: '#797979',
      fontSize: '14px',
      fontFamily: 'Inter, sans-serif',
    },
  },
  cross: {
    border: 'none',
    background: 'none',
    padding: 0,
    margin: 0,
    cursor: 'pointer',
  },
})
