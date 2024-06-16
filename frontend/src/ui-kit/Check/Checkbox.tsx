import {createUseStyles} from 'react-jss'

const useStyles = createUseStyles({
  checkbox: {
    flexShrink: 0,
    width: 20,
    height: 20,
    borderRadius: 8,
    border: '2px solid #ccc',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    cursor: 'pointer',
    transition: 'all 0.3s',
  },
  checked: {
    backgroundColor: '#00a7b2',
    borderColor: '#00a7b2',
  },
  svg: {
    width: '50%',
    height: '50%',
  },
})

const CheckBox = ({active}: {active?: boolean}) => {
  const classes = useStyles()

  return (
    <div className={`${classes.checkbox} ${active ? classes.checked : ''}`}>
      {active && (
        <svg xmlns='http://www.w3.org/2000/svg' width='18' height='18' fill='none' viewBox='0 0 18 18'>
          <path
            fill='#fff'
            fillRule='evenodd'
            d='M15.7 4.522a.833.833 0 010 1.179l-7.777 7.777a.833.833 0 01-1.179 0L2.855 9.59A.833.833 0 114.034 8.41l3.3 3.3 7.188-7.189a.833.833 0 011.178 0z'
            clipRule='evenodd'
          ></path>
        </svg>
      )}
    </div>
  )
}

export default CheckBox
