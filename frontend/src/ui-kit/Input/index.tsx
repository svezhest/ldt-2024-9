import {FC} from 'react'
import {createUseStyles} from 'react-jss'

type InputProps = {
  placeholder?: string
  readOnly?: boolean
  text?: string
  setText?: (arg: string) => void
}

export const Input: FC<InputProps> = ({placeholder, readOnly, text, setText}) => {
  const c = useStyles()

  return (
    <input
      className={c.input}
      placeholder={placeholder}
      readOnly={readOnly}
      onChange={(event) => setText?.(event.target.value)}
      value={text}
    />
  )
}

const useStyles = createUseStyles({
  input: {
    marginTop: 5,
    width: '100%',
    padding: [15, 20],
    backgroundColor: '#F8F8F8',
    borderRadius: 12,
    marginBottom: 20,
    boxSizing: 'border-box',

    '&::placeholder': {
      color: 'rgba(121, 121, 121, 1)',
      fontSize: 14,
    },
  },
})
