import {Search} from './Search'
import {createUseStyles} from 'react-jss'

export const SearchInput = () => {
  const c = useStyles()

  return (
    <div className={c.pos}>
      <input className={c.search} placeholder='Введите текст...' />
      <div className={c.searchLogo}>
        <Search />
      </div>
    </div>
  )
}

const useStyles = createUseStyles({
  pos: {
    position: 'relative',
    width: 'fit-content',
  },
  searchLogo: {
    position: 'absolute',
    right: 20,
    top: 15,
  },
  search: {
    backgroundColor: 'rgba(248, 248, 248, 1)',
    borderRadius: 12,
    padding: 20,
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    fontSize: 14,

    '& ::placeholder': {
      color: 'rgba(121, 121, 121, 1)',
    },
  },
})
