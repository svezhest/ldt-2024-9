import {createUseStyles} from 'react-jss'
import CheckBox from './Checkbox'
import {FC, useState} from 'react'

type CheckProps = {
  readOnly?: boolean
  text?: string
}

export const Check: FC<CheckProps> = ({readOnly, text}) => {
  const c = useStyles()
  const [checked, setChecked] = useState(true)

  const toggleCheck = () => {
    if (readOnly) {
      return
    }
    setChecked(!checked)
  }

  return (
    <div className={c.checks} onClick={toggleCheck}>
      <CheckBox active={checked} />
      <p className={c.checkTitle}>{text}</p>
    </div>
  )
}

const useStyles = createUseStyles({
  checks: {
    display: 'flex',
    gap: 20,
    paddingRight: 28,
    marginTop: 15,
    alignItems: 'center',
    cursor: 'pointer',
  },
  checkTitle: {
    color: '#757575',
    fontSize: 14,
  },
})
