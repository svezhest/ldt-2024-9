import classNames from 'classnames'
import {FC} from 'react'
import {createUseStyles} from 'react-jss'
import {ArrowLeft} from '../'

type ArrowsProps = {
  leftFunc?: () => void
  rightFunc?: () => void
}

export const Arrows: FC<ArrowsProps> = ({leftFunc, rightFunc}) => {
  const c = useStyles()

  return (
    <div className={c.crosses}>
      <button className={c.arrow} onClick={leftFunc}>
        <ArrowLeft />
      </button>
      <button className={classNames(c.arrow, c.rotate)} onClick={rightFunc}>
        <ArrowLeft />
      </button>
    </div>
  )
}

const useStyles = createUseStyles({
  crosses: {
    display: 'flex',
    gap: 10,
  },
  arrow: {
    backgroundColor: 'rgba(248, 248, 248, 1)',
    borderRadius: 12,
    padding: 6,
    cursor: 'pointer',
    '&:active': {
      backgroundColor: 'white',
    },
  },
  rotate: {
    transform: 'rotate(180deg)',
  },
})
