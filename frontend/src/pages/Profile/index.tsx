import React, {useEffect, useState} from 'react'
import {createUseStyles} from 'react-jss'
import {RootState} from '../../storage/store'
import {useSelector} from 'react-redux'
import {Check, Input} from '../../ui-kit'
import {getDoctor} from '../../api'
import {Skills} from '../../api/types'

export const Profile = () => {
  const c = useStyles()
  const account = useSelector((state: RootState) => state.account)
  const [skills, setSkills] = useState<null | Skills>(null)

  useEffect(() => {
    if (account.id && account.token) {
      getDoctor(account.id, account.token).then((res) => {
        setSkills(res.skills)
        return
      })
    }
  }, [])

  return (
    <div className={c.root}>
      <h1 className={c.header}>Личная информация</h1>
      <div className={c.content}>
        <p className={c.title}>ФИО</p>
        <Input placeholder={account.fullName} readOnly />
        <p className={c.title}>Должность</p>
        <Input placeholder={account.position} readOnly />
        <p className={c.title}>Специализация</p>
        <Input placeholder={account.specialization} readOnly />
        <p className={c.title}>Компетенции</p>
        <Check readOnly text={skills?.primary_skill} />
        {skills?.secondary_skills.map((el, i) => <Check key={i} readOnly text={el} />)}
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
})
