import {createUseStyles} from 'react-jss'
import {DoctorCard} from './Card'
// import {data} from './Card/mock'
import {Dropdown, SearchInput, ColoredButton} from '../../ui-kit'
import {useEffect, useState} from 'react'
import {RootState} from '../../storage/store'
import {useSelector} from 'react-redux'
import {getDoctors} from '../../api'
import {DoctorPublicInfo} from '../../api/types'
import {useNavigate} from 'react-router-dom'

export const Doctors = () => {
  const c = useStyles()
  const account = useSelector((state: RootState) => state.account)
  const [data, setDoctors] = useState<DoctorPublicInfo[] | null>(null)
  const navigate = useNavigate()

  useEffect(() => {
    if (account.token) {
      getDoctors(account.token).then((res) => {
        setDoctors(res)
        return
      })
    }
  }, [])

  return (
    <div className={c.root}>
      <div className={c.heading}>
        <SearchInput />
        <Dropdown text='Специализация' />
        <Dropdown text='Работает' />
        <ColoredButton text='Добавить нового специалиста' onClick={() => navigate('/add_doctors')} />
      </div>
      <div className={c.cards}>
        {data &&
          data.map((el, i) => (
            <DoctorCard
              busy='available'
              fullName={el.full_name}
              jobTitle={el.position}
              competitions={el.specialization}
              key={i}
            />
          ))}
      </div>
    </div>
  )
}

const useStyles = createUseStyles({
  root: {
    padding: [30, 80, 30, 50],
  },
  heading: {
    display: 'flex',
    gap: 10,
  },
  cards: {
    display: 'flex',
    gap: 10,
    marginTop: 25,
    flexWrap: 'wrap',
  },
})
