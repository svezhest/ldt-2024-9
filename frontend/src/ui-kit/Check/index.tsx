/* eslint-disable @typescript-eslint/no-unused-vars */
import {createUseStyles} from 'react-jss'
import CheckBox from './Checkbox'
import {FC, useState} from 'react'

type CheckProps = {
  readOnly?: boolean
  text?: string
  workload?: Record<string, boolean>
  setWorkload?: (arg: Record<string, boolean>) => void
}

export const Check: FC<CheckProps> = ({readOnly, text, workload, setWorkload}) => {
  const c = useStyles()
  const [checked, setChecked] = useState(workload ? Boolean(workload[`${text}`]) : false)

  const toggleCheck = () => {
    if (readOnly) {
      return
    }
    setChecked(!checked)
    if (workload && setWorkload && text) {
      setWorkload({...workload, [text]: !workload[text]})

      // eslint-disable-next-line no-console
      console.log(workload, text)
    }
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
