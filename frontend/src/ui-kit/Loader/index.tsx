import {createUseStyles} from 'react-jss'

export const Loader = () => {
  const c = useStyles()

  return (
    <div className={c.root}>
      <svg
        className={c.svg}
        xmlns='http://www.w3.org/2000/svg'
        width='800'
        height='800'
        fill='none'
        viewBox='0 0 24 24'
      >
        <path
          className={c.circle}
          stroke='#000'
          strokeLinecap='round'
          strokeLinejoin='round'
          strokeWidth='2'
          d='M12 3v3m0 12v3m-6-9H3m18 0h-3M5.637 5.637L7.76 7.76m8.482 8.482l2.121 2.121m.002-12.728l-2.12 2.12m-8.487 8.487l-2.123 2.123'
        ></path>
      </svg>
    </div>
  )
}

const useStyles = createUseStyles({
  root: {
    height: '100%',
    width: '100%',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
  },
  svg: {
    width: 50,
    height: 50,
  },
  '@keyframes spin': {
    from: {
      transform: 'rotate(0deg)',
    },
    to: {
      transform: 'rotate(360deg)',
    },
  },
  circle: {
    animation: 'spin 10s linear infinite',
  },
})
