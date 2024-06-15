import React, {FC} from 'react'

type CrossProps = {
  color?: 'red' | 'green'
}

export const Cross: FC<CrossProps> = ({color}) => {
  return (
    <svg xmlns='http://www.w3.org/2000/svg' width='24' height='24' fill='none' viewBox='0 0 24 24'>
      <path
        fill={color === 'red' ? 'rgba(240, 47, 47, 1)' : '#58B3C0'}
        d='M19 11h-6V5a1 1 0 00-2 0v6H5a1 1 0 000 2h6v6a1 1 0 002 0v-6h6a1 1 0 000-2z'
      ></path>
    </svg>
  )
}
