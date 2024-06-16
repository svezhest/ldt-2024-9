import {useNavigate} from 'react-router-dom'
import {BlueButton, Check, Date, Dropdown, Input} from '../../ui-kit'
import {createUseStyles} from 'react-jss'
import {Arrow} from './Arrow'
import classNames from 'classnames'
import {createDoctor} from '../../api'
import {useSelector} from 'react-redux'
import {RootState} from '../../storage/store'
import {useState} from 'react'
import {DoctorTechnicalInfo} from '../../api/types'

export const AddDoctor = () => {
  const c = useStyles()
  const navigate = useNavigate()
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const account = useSelector((state: RootState) => state.account)

  const sendCreateDoctor = () => {
    if (!account.token) {
      return
    }

    const doctor: DoctorTechnicalInfo = {
      full_name: name,
      email,
      password,
      phone_number: '+79995680017',
      role: 'doctor',
      account_status: 'ok',
      skills: {
        primary_skill: 'ct',
        secondary_skills: ['mri'],
      }, //fix
      specialization: '',
      position: '',
      date_of_birth: '2003-05-23',
      hours_per_week: 40,
      shifting_type: '5/2',
      start_hours: '08:00',
    }

    createDoctor(doctor, account.token).then(() => {
      navigate('/doctors')
    })
  }

  return (
    <div className={c.root}>
      <div className={c.heading}>
        <button className={c.arrow} onClick={() => navigate('/doctors')}>
          <Arrow />
        </button>
        <h1 className={c.header}>Добавление нового врача</h1>
      </div>
      <div className={c.content}>
        <div className={c.leftSide}>
          <p className={c.text}>ФИО врача</p>
          <Input placeholder='Введите текст' text={name} setText={setName} />
          <p className={c.text}>Должность</p>
          <Dropdown text='Врач' className={c.dropdown} />
          <p className={c.text}>Специализация</p>
          <Dropdown text='Врач-рентолог' className={c.dropdown} />
          <h3 className={c.h3}>Данные личного кабинета врача</h3>
          <p className={c.text}>Email</p>
          <Input placeholder='Введите почту' text={email} setText={setEmail} />
          <p className={c.text}>Пароль</p>
          <Input placeholder='Введите пароль' text={password} setText={setPassword} />
          <BlueButton isInverse text='Отправить' className={c.button} onClick={sendCreateDoctor} />
        </div>
        <div className={c.rightSide}>
          <p className={c.text}>График работы</p>
          <div className={c.dates}>
            <Date text='30.06' type='available' />
          </div>
          <BlueButton text='Выбрать смены' className={c.button} />
          <p className={classNames(c.text, c.textMargin)}>Компетенции</p>
          <Check text='Проведение рентгенологических  исследований (в том числе  компьютерных томографических) и  магнитно-резонанснотомографических исследований  органов и систем организма  человека' />
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
  dates: {
    marginTop: 10,
    display: 'flex',
  },
  content: {
    marginTop: 35,
    display: 'grid',
    gridTemplateColumns: '40% 60%',
    gridTemplateRows: '1fr',
    gridColumnGap: 40,
    gridRowGap: 0,
  },
  leftSide: {
    gridArea: '1 / 1 / 2 / 2',
  },
  rightSide: {
    gridArea: '1 / 2 / 2 / 3',
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
  h3: {
    marginTop: 30,
    marginBottom: 20,
  },
  textMargin: {
    marginTop: 40,
  },
})
