import {FC} from 'react'
import {createUseStyles} from 'react-jss'

type ButtonProps = {
  isActive?: boolean
  onClick?: () => void
  text?: string
}

type ButtonSliderProps = {
  first?: ButtonProps
  second?: ButtonProps
  third?: ButtonProps
}

export const ButtonSlider: FC<ButtonSliderProps> = ({first, second, third}) => {
  const c = useStyles()

  return (
    <div className={c.buttonGroup}>
      <button className={`${c.button} ${first?.isActive ? c.activeButton : undefined}`} onClick={first?.onClick}>
        {first?.text}
      </button>
      <button className={`${c.button} ${second?.isActive ? c.activeButton : undefined}`} onClick={second?.onClick}>
        {second?.text}
      </button>
      <button className={`${c.button} ${third?.isActive ? c.activeButton : undefined}`} onClick={third?.onClick}>
        {third?.text}
      </button>
    </div>
  )
}

const useStyles = createUseStyles({
  buttonGroup: {
    display: 'flex',
    gap: 8,
    backgroundColor: 'rgba(248, 248, 248, 1)',
    padding: 8,
    borderRadius: 12,
    width: 'fit-content',
  },
  activeButton: {
    backgroundColor: 'white !important',
  },
  button: {
    padding: [5, 12],
    fontSize: 12,
    border: 'none',
    borderRadius: 8,
    cursor: 'pointer',
    backgroundColor: 'transparent',
    '&:hover': {
      backgroundColor: 'white',
    },
    '&:active': {
      backgroundColor: 'white',
    },
  },
})
