import {ColoredButton, Dropdown, SearchInput} from '../../ui-kit'
import {createUseStyles} from 'react-jss'
import { Card } from './Card'

export const Absence = () => {
  const c = useStyles()

  return (
    <div className={c.root}>
      <div className={c.heading}>
        <SearchInput />
        <Dropdown text='Специализация' />
        <ColoredButton text='Добавить непредвиденное обстоятельство' color='red' />
      </div>
      <div className={c.cards}>
        <Card type='sickness' />
        <Card type='vacation' />
        <Card type='absence' />
      </div>
    </div>
  )
}

const useStyles = createUseStyles({
  root: {
    padding: [30, 50],
  },
  heading: {
    display: 'flex',
    gap: 10,
  },
  cards: {
    marginTop: 25,
    gap: 10,
    display: 'flex',
  },
})
