import React from 'react'
import {createUseStyles} from 'react-jss'
import CheckBox from './Checkbox'
import {RootState} from '../../storage/store'
import {useSelector} from 'react-redux'

export const Profile = () => {
  const c = useStyles()
  const account = useSelector((state: RootState) => state.account)
  account.skills

  return (
    <div className={c.root}>
      <h1 className={c.header}>Личная информация</h1>
      <div className={c.content}>
        <p className={c.title}>ФИО</p>
        <input className={c.input} placeholder={account.fullName} readOnly />
        <p className={c.title}>Должность</p>
        <input className={c.input} placeholder={account.role} readOnly />
        <p className={c.title}>Специализация</p>
        <input className={c.input} placeholder={account.specialization} readOnly />
        <p className={c.title}>Компетенции</p>
        <div className={c.checks}>
          <CheckBox />
          <p className={c.checkTitle}>{account.skills?.primary_skill}</p>
          {account.skills?.secondary_skills.map((el, i) => (
            <p key={i} className={c.checkTitle}>
              {el}
            </p>
          ))}
        </div>
      </div>
    </div>
  )
}

const useStyles = createUseStyles({
  root: {
    padding: [40, 80, 40, 50],
    fontFamily: 'Inter, sans-serif',
  },
  header: {
    fontSize: 28,
    fontWeight: 600,
  },
  title: {
    fontSize: 14,
    paddingLeft: 10,
  },
  content: {
    marginTop: 35,
  },
  input: {
    marginTop: 5,
    width: '100%',
    padding: [15, 20],
    backgroundColor: '#F8F8F8',
    borderRadius: 12,
    marginBottom: 20,

    '&::placeholder': {
      color: 'black',
      fontSize: 14,
    },
  },
  checks: {
    display: 'flex',
    gap: 20,
    paddingRight: 28,
    marginTop: 15,
    alignItems: 'center',
  },
  radio: {},
  checkTitle: {
    color: '#757575',
    fontSize: 14,
  },
})
