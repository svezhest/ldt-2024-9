import React, {FC, ReactElement} from 'react'
import {createUseStyles} from 'react-jss'
import cn from 'classnames'

type ButtonProps = {
  children?: ReactElement
  text?: string
  isActive?: boolean
  onClick?: () => void
}

export const Button: FC<ButtonProps> = ({children, text, isActive, onClick}) => {
  const c = useStyles()

  return (
    <div className={cn(c.root, isActive && c.active)} onClick={onClick}>
      {children}
      <p className={c.text}>{text}</p>
    </div>
  )
}

const useStyles = createUseStyles({
  root: {
    borderRadius: 8,
    gap: 16,
    display: 'flex',
    padding: [8, 16],
    alignItems: 'center',
    cursor: 'pointer',

    '&:active': {
      backgroundColor: '#E6F5F7',
    },
  },
  active: {
    backgroundColor: '#E6F5F7',
  },
  text: {
    fontSize: 16,
    fontWeight: 500,
    fontFamily: 'Inter, sans-serif',
    textOverflow: 'ellipsis',
    whiteSpace: 'nowrap',
    overflow: 'hidden',
  },
})
