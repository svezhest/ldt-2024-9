import {createUseStyles} from 'react-jss'
import {Cross} from './Cross'
import {FC} from 'react'
import classNames from 'classnames'

type ColoredButtonProps = {
  text?: string
  color?: 'red' | 'green'
  onClick?: () => void
}

export const ColoredButton: FC<ColoredButtonProps> = ({text, color, onClick}) => {
  const c = useStyles()

  return (
    <button className={classNames(c.addNewDoctor, color === 'red' ? c.red : c.green)} onClick={onClick}>
      <p>{text}</p>
      <Cross color={color === 'red' ? 'red' : 'green'} />
    </button>
  )
}

const useStyles = createUseStyles({
  addNewDoctor: {
    display: 'flex',
    alignItems: 'center',
    borderRadius: 12,
    padding: [16.5, 20],
    fontSize: 14,
    justifyContent: 'space-between',
    gap: 8,
    cursor: 'pointer',
    fontFamily: 'Inter, sans-serif',
  },
  green: {
    backgroundColor: 'rgba(230, 245, 247, 1)',
    color: 'rgba(88, 179, 192, 1)',
  },
  red: {
    color: 'rgba(240, 47, 47, 1)',
    backgroundColor: 'rgba(255, 226, 226, 1)',
  },
})
