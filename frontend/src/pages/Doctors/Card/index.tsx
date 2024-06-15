import {createUseStyles} from 'react-jss'
import {Edit} from './Edit'
import {FC} from 'react'
import classNames from 'classnames'

type DoctorCardProps = {
  busy: string
  fullName: string
  competitions: string
  jobTitle: string
  dates?: {
    date: string
    type: string
  }
}

const status: {[key: string]: string} = {
  available: 'работает',
  sickness: 'болеет',
  vacation: 'в отпуске',
}

const statusAction: {[key: string]: string} = {
  available: 'Добавить смену',
  sickness: 'Вывести из больничнего',
  vacation: 'Вывести из отпуска',
}

export const DoctorCard: FC<DoctorCardProps> = ({busy, fullName, jobTitle, competitions}) => {
  const c = useStyles()

  return (
    <div className={c.root}>
      <div className={c.heading}>
        <h3>{fullName}</h3>
        <Edit />
      </div>
      <p className={c.jobTitle}>{jobTitle}</p>
      <div className={c.buttons}>
        <p
          className={classNames(
            c.leftButton,
            busy === 'sickness'
              ? c.leftButtonOnSickness
              : busy === 'vacation'
                ? c.leftButtonOnVacation
                : c.leftButtonOnWork
          )}
        >
          Статус: {status[busy as keyof typeof status]}
        </p>
        <button
          className={classNames(
            c.rightButton,
            busy === 'sickness'
              ? c.rightButtonOnSickness
              : busy === 'vacation'
                ? c.rightButtonOnVacation
                : c.rightButtonOnWork
          )}
        >
          {statusAction[busy as keyof typeof status]}
        </button>
      </div>
      <p className={c.competitions}>{competitions}</p>
      <div className={c.dates}>
        <p className={c.date}>29.06</p>
        {busy === 'available' && <p className={classNames(c.date, c.activeDate)}>30.06</p>}
      </div>
    </div>
  )
}

const useStyles = createUseStyles({
  root: {
    boxShadow: '0px 0px 10px 0px rgba(0,0,0,0.2)',
    padding: [20, 30],
    fontFamily: 'Inter, sans-serif',
    borderRadius: 12,
    flexShrink: 0,
    width: '43%',
  },
  heading: {
    display: 'flex',
    justifyContent: 'space-between',
    fontWeight: 500,
    fontSize: 18,
  },
  jobTitle: {
    marginTop: 5,
  },
  buttons: {
    marginTop: 20,
    display: 'flex',
    gap: 10,
  },
  leftButton: {
    fontSize: 14,
    fontWeight: 600,
    padding: [12, 20],
    borderRadius: 12,
  },
  leftButtonOnSickness: {
    backgroundColor: 'rgba(255, 226, 226, 1)',
    color: 'rgba(240, 47, 47, 1)',
  },
  leftButtonOnVacation: {
    backgroundColor: 'rgba(255, 236, 222, 1)',
    color: 'rgba(247, 156, 91, 1)',
  },
  leftButtonOnWork: {
    backgroundColor: 'rgba(230, 245, 247, 1)',
    color: 'rgba(88, 179, 192, 1)',
  },
  rightButton: {
    backgroundColor: 'rgba(88, 179, 192, 1)',
    color: 'white',
    padding: [12, 20],
    borderRadius: 12,
    fontSize: 14,
    fontWeight: 600,
    cursor: 'pointer',
  },
  rightButtonOnSickness: {
    backgroundColor: 'rgba(240, 47, 47, 1)',
    color: 'white',
  },
  rightButtonOnVacation: {
    backgroundColor: 'rgba(247, 156, 91, 1)',
    color: 'white',
  },
  rightButtonOnWork: {
    backgroundColor: 'rgba(88, 179, 192, 1)',
    color: 'white',
  },
  competitions: {
    marginTop: 20,
    fontSize: 12,
  },
  dates: {
    marginTop: 20,
    display: 'flex',
    gap: 5,
  },
  date: {
    padding: [10, 12.5],
    fontSize: 14,
    backgroundColor: 'rgba(248, 248, 248, 1)',
    borderRadius: 12,
    cursor: 'pointer',
  },
  activeDate: {
    backgroundColor: 'rgba(230, 245, 247, 1)',
  },
})

// box-shadow: 0px 0px 10px 0px rgba(0,0,0,0.2);
