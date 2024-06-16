import {BlueButton, ArrowLeft} from '../../ui-kit'
import React, {useState} from 'react'
import {createUseStyles} from 'react-jss'
import cn from 'classnames'
import {useNavigate} from 'react-router-dom'
import {getMyself, loginForAccessToken} from '../../api'
import {useDispatch} from 'react-redux'
import {AppDispatch} from '../../storage/store'
import {setAccountData} from '../../storage/accountSlice'

type AuthSecondProps = {
  profile: 'doctor' | 'HR' | 'head'
}

export const AuthSecond: React.FC<AuthSecondProps> = () => {
  const c = useStyles()
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const dispatch = useDispatch<AppDispatch>()

  const auth = () => {
    if (!email || !password) {
      return
    }
    loginForAccessToken(email, password).then((res) => {
      dispatch(
        setAccountData({
          token: res.access_token,
        })
      )

      const expiryDate = new Date()
      expiryDate.setDate(expiryDate.getDate() + 7)
      document.cookie = `jwtToken=${JSON.stringify({token: res.access_token, expiry: expiryDate.getTime()})}; expires=${expiryDate.toUTCString()}; path=/`

      // by_sheer_willpower"

      getMyself(res.access_token).then((res) => {
        dispatch(
          setAccountData({
            id: res.id,
            fullName: res.full_name,
            dateOfBirth: res.date_of_birth,
            position: res.position,
            specialization: res.specialization,
          })
        )
        navigate('/profile')
      })
    })
  }

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
        <input
          className={c.input}
          placeholder='Введите почту'
          type='email'
          value={email}
          onChange={(event) => setEmail(event.target.value)}
        />
        <p className={c.inputHeader}>Пароль</p>
        <input
          className={c.input}
          placeholder='Введите пароль'
          type='password'
          value={password}
          onChange={(event) => setPassword(event.target.value)}
        />
        <BlueButton className={c.button} text='Войти' size='md' isInverse onClick={auth} />
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
