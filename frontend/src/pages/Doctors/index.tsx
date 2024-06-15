import {createUseStyles} from 'react-jss'
import {DoctorCard} from './Card'
import {data} from './Card/mock'
import {Dropdown, SearchInput, ColoredButton} from '../../ui-kit'

export const Doctors = () => {
  const c = useStyles()

  return (
    <div className={c.root}>
      <div className={c.heading}>
        <SearchInput />
        <Dropdown text='Специализация' />
        <Dropdown text='Работает' />
        <ColoredButton text='Добавить нового специалиста' />
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
