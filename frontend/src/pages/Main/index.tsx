import React, {FC, ReactElement} from 'react'
import {createUseStyles} from 'react-jss'
import {Button} from './Button'
import {Calendar, Profile, Job, Settings, Warning, Doctors, Detect} from './Button/logos'
import {useLocation, useNavigate} from 'react-router-dom'
import {RootState} from '../../storage/store'
import {useSelector} from 'react-redux'

type MainProps = {
  children?: ReactElement
}

export const Main: FC<MainProps> = ({children}) => {
  const c = useStyles()
  const location = useLocation()
  const navigate = useNavigate()
  const account = useSelector((state: RootState) => state.account)

  return (
    <div className={c.root}>
      <div className={c.leftPart}>
        <div className={c.bio}>
          <p className={c.name}>{account.fullName}</p>
          <p className={c.job}>{account.specialization}</p>
          <p className={c.badge}>{account.position}</p>
        </div>
        <div className={c.buttons}>
          <Button text='Мой профиль' isActive={location.pathname === '/profile'} onClick={() => navigate('/profile')}>
            <Profile />
          </Button>
          <Button text='График' isActive={location.pathname === '/calendar'} onClick={() => navigate('/calendar')}>
            <Calendar />
          </Button>
          <Button text='Работа' isActive={location.pathname === '/job'} onClick={() => navigate('/job')}>
            <Job />
          </Button>
          <Button text='Прогноз' isActive={location.pathname === '/detect'} onClick={() => navigate('/detect')}>
            <Detect />
          </Button>
          <Button text='Врачи' isActive={location.pathname === '/doctors'} onClick={() => navigate('/doctors')}>
            <Doctors />
          </Button>
          <Button
            text='Непредвиденные обстоятельства'
            isActive={location.pathname === '/absence'}
            onClick={() => navigate('/absence')}
          >
            <Warning />
          </Button>
          <Button text='Настройки' isActive={location.pathname === '/settings'} onClick={() => navigate('/settings')}>
            <Settings />
          </Button>
        </div>
      </div>
      <div className={c.rightPart}>{children}</div>
    </div>
  )
}

const useStyles = createUseStyles({
  root: {
    display: 'grid',
    gridTemplateColumns: '270px 1fr',
    gridTemplateRows: '1fr',
    gridColumnGap: 0,
    gridRowGap: 0,
  },
  leftPart: {
    gridArea: '1 / 1 / 2 / 2',
    padding: [25, 8],
    borderRight: '1px solid #F8F8F8',
    height: '100vh',
  },
  rightPart: {
    gridArea: '1 / 2 / 2 / 3',
  },
  name: {
    fontSize: 20,
    fontWeight: 600,
    fontFamily: 'Inter, sans-serif',
    lineHeight: '30px',
  },
  job: {
    fontSize: 12,
    fontFamily: 'Inter, sans-serif',
    lineHeight: '18px',
  },
  bio: {
    padding: [0, 18],
  },
  badge: {
    padding: [10, 15],
    color: '#58B3C0',
    fontSize: 14,
    fontFamily: 'Inter, sans-serif',
    backgroundColor: '#E6F5F7',
    width: 98,
    borderRadius: 12,
    textAlign: 'center',
    marginTop: 10,
  },
  buttons: {
    margin: [32, 0],
  },
})
