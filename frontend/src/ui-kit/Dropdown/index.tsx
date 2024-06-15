import {FC} from 'react'
import {Arrow} from './Arrow'
import {createUseStyles} from 'react-jss'

type DropdownProps = {
  text: string
}

export const Dropdown: FC<DropdownProps> = ({text}) => {
  const c = useStyles()

  return (
    <button className={c.button}>
      <p>{text}</p>
      <Arrow />
    </button>
  )
}

const useStyles = createUseStyles({
  button: {
    backgroundColor: 'rgba(248, 248, 248, 1)',
    borderRadius: 12,
    padding: [15, 20],
    display: 'flex',
    justifyContent: 'space-between',
    gap: 20,
    alignItems: 'center',
    fontSize: 14,
    color: 'rgba(121, 121, 121, 1)',
    cursor: 'pointer',
  },
})
