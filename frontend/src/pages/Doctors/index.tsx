import {createUseStyles} from 'react-jss'
import {DoctorCard} from './Card'
import {Cross, Search} from './Logos'
import {data} from './Card/mock'
import {Dropdown} from '../../ui-kit'

export const Doctors = () => {
  const c = useStyles()

  return (
    <div className={c.root}>
      <div className={c.heading}>
        <div className={c.pos}>
          <input className={c.search} placeholder='Введите текст...' />
          <div className={c.searchLogo}>
            <Search />
          </div>
        </div>
        <Dropdown text='Специализация' />
        <Dropdown text='Работает' />
        <button className={c.addNewDoctor}>
          <p className={c.addNewDoctorText}>Добавить нового специалиста</p>
          <Cross />
        </button>
      </div>
      <div className={c.cards}>
        {data.map((el, i) => (
          <DoctorCard
            busy={el.busy}
            fullName={el.fullName}
            jobTitle={el.jobTitle}
            competitions={el.competitions}
            dates={el.dates}
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
  pos: {
    position: 'relative',
    width: 'fit-content',
  },
  searchLogo: {
    position: 'absolute',
    right: 20,
    top: 15,
  },
  heading: {
    display: 'flex',
    gap: 10,
  },
  search: {
    backgroundColor: 'rgba(248, 248, 248, 1)',
    borderRadius: 12,
    padding: 20,
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    fontSize: 14,

    '& ::placeholder': {
      color: 'rgba(121, 121, 121, 1)',
    },
  },
  addNewDoctor: {
    backgroundColor: 'rgba(230, 245, 247, 1)',
    color: 'rgba(88, 179, 192, 1)',
    display: 'flex',
    alignItems: 'center',
    borderRadius: 12,
    padding: [16.5, 20],
    fontSize: 14,
    justifyContent: 'space-between',
    gap: 8,
    cursor: 'pointer',
  },
  addNewDoctorText: {},
  cards: {
    display: 'flex',
    gap: 10,
    marginTop: 25,
    flexWrap: 'wrap',
  },
})
