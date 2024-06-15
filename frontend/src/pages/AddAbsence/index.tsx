import {useNavigate} from 'react-router-dom'
import {BlueButton, Dropdown} from '../../ui-kit'
import {createUseStyles} from 'react-jss'
import {Arrow} from './Arrow'

export const AddAbsence = () => {
  const c = useStyles()
  const navigate = useNavigate()

  return (
    <div className={c.root}>
      <div className={c.heading}>
        <button className={c.arrow} onClick={() => navigate('/absence')}>
          <Arrow />
        </button>
        <h1 className={c.header}>Добавление непредвиденных обстоятельств</h1>
      </div>
      <div className={c.content}>
        <p className={c.text}>ФИО врача</p>
        <Dropdown text='Выберите из списка' className={c.dropdown} />
        <p className={c.text}>Тип обстоятельства</p>
        <Dropdown text='Выберите из списка' className={c.dropdown} />
        <div>
          <p className={c.text}>Рабочие смены</p>
          <p className={c.subText}>Выберите дни, в которые не сможете выходить на работу</p>
          <BlueButton text='Выбрать смены' className={c.button} />
        </div>
        <div className={c.buttonWrapper}>
          <BlueButton isInverse text='Отправить' className={c.button} />
        </div>
      </div>
    </div>
  )
}

const useStyles = createUseStyles({
  root: {
    padding: [40, 50],
    fontFamily: 'Inter, sans-serif',
  },
  heading: {
    display: 'flex',
    gap: 10,
    alignItems: 'center',
  },
  arrow: {
    backgroundColor: 'transparent',
  },
  header: {
    fontSize: 28,
  },
  content: {
    marginTop: 35,
  },
  text: {
    fontSize: 14,
  },
  subText: {
    fontSize: 12,
    color: 'rgba(153, 153, 153, 1)',
  },
  dropdown: {
    marginTop: 5,
    marginBottom: 20,
    width: '30vw',
  },
  button: {
    marginTop: 15,
    width: '300px !important',
  },
  buttonWrapper: {
    marginTop: 40,
  },
})
