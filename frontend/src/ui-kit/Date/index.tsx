import classNames from 'classnames'
import {FC} from 'react'
import {createUseStyles} from 'react-jss'

type DateProps = {
  type: 'vacation' | 'sickness' | 'available' | 'absence'
  text: string
}

export const Date: FC<DateProps> = ({type, text}) => {
  const c = useStyles()
  return (
    <p
      className={classNames(
        c.date,
        type === 'vacation' ? c.vacationDate : type === 'sickness' ? c.sicknessDate : c.absenceDate
      )}
    >
      {text}
    </p>
  )
}

const useStyles = createUseStyles({
  date: {
    padding: [5, 12.5],
    borderRadius: 12,
  },
  vacationDate: {
    backgroundColor: 'rgba(255, 236, 222, 1)',
  },
  sicknessDate: {
    backgroundColor: 'rgba(255, 226, 226, 1)',
  },
  absenceDate: {
    backgroundColor: 'rgba(248, 248, 248, 1)',
  },
})
