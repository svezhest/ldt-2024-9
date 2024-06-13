import React, {FC, ReactElement, useState} from 'react'
import {createUseStyles} from 'react-jss'
import cn from 'classnames'

type ChildProps = {
  isHovered?: boolean
}

type BlueButton = {
  size?: 'lg' | 'md' | 'sm'
  text?: string
  children?: ReactElement<ChildProps>
  onClick?: () => void
  className?: string
  isInverse?: boolean
}

export const BlueButton: FC<BlueButton> = ({size = 'lg', children, text, onClick, className, isInverse}) => {
  const c = useStyles()
  const [isHovered, setIsHovered] = useState(false)
  const enhancedChildren = React.isValidElement(children) ? React.cloneElement(children, {isHovered}) : children

  const handleMouseEnter = () => {
    setIsHovered(true)
  }

  const handleMouseLeave = () => {
    setIsHovered(false)
  }

  return (
    <button
      className={cn(c.root, className, isInverse ? c.inverse : null)}
      onClick={onClick}
      style={{width: size === 'lg' ? '40vw' : undefined}}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
    >
      {enhancedChildren}
      <p>{text}</p>
    </button>
  )
}

const useStyles = createUseStyles({
  root: {
    padding: [17, 39],
    backgroundColor: '#E6F5F7',
    color: '#58B3C0',
    borderRadius: 12,
    gap: 14,
    maxWidth: 388,
    fontSize: 16,
    lineHeight: '24px',
    fontWeight: 600,
    fontFamily: 'Inter, sans-serif',
    justifyContent: 'flex-start',
    display: 'flex',
    alignItems: 'center',
    cursor: 'pointer',

    '&:hover': {
      background: '#58B3C0',
      color: 'white',
    },
  },

  inverse: {
    background: '#58B3C0',
    color: 'white',
    justifyContent: 'center',
    fontSize: 14,
    padding: [12, 39],

    '&:active': {
      background: '#E6F5F7',
      color: '#58B3C0',
    },
  },
})
