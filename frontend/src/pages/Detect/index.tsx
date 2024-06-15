import classNames from 'classnames'
import {Arrows} from '../../ui-kit'
import {createUseStyles} from 'react-jss'

export const Detect = () => {
  const c = useStyles()

  return (
    <div className={c.root}>
      <div className={c.heading}>
        <Arrows />
        <h2 className={c.title}>3.06 - 09.06</h2>
      </div>
      <table className={c.table}>
        <tr className={c.tableHeading}>
          <td className={c.tableHeadingCell}>Тип</td>
          <td className={c.tableHeadingCell}>Сделано</td>
          <td className={c.tableHeadingCell}>Будет сделано за неделю (прогноз)</td>
          <td className={c.tableHeadingCell}>Нужно сделать исследований (прогноз)</td>
          <td className={c.tableHeadingCell}>Рекомендация</td>
        </tr>
        <tr className={classNames(c.tableRow, c.sickness)}>
          <td className={c.tableCell}>КТ</td>
          <td className={c.tableCell}>200</td>
          <td className={c.tableCell}>4000</td>
          <td className={c.tableCell}>5000</td>
          <td className={c.tableCell}>Переназначить врачей</td>
        </tr>
        <tr className={classNames(c.tableRow, c.work)}>
          <td className={c.tableCell}>КТ</td>
          <td className={c.tableCell}>200</td>
          <td className={c.tableCell}>4000</td>
          <td className={c.tableCell}>5000</td>
          <td className={c.tableCell}>Переназначить врачей</td>
        </tr>
        <tr className={c.tableRow}>
          <td className={c.tableCell}>КТ</td>
          <td className={c.tableCell}>1000</td>
          <td className={c.tableCell}>4000</td>
          <td className={c.tableCell}>4000</td>
          <td className={c.tableCell}>-</td>
        </tr>
        <tr className={classNames(c.tableRow, c.vacation)}>
          <td className={c.tableCell}>Рентген</td>
          <td className={c.tableCell}>200</td>
          <td className={c.tableCell}>4000</td>
          <td className={c.tableCell}>5000</td>
          <td className={c.tableCell}>Вызвать врача из отпуска</td>
        </tr>
      </table>
    </div>
  )
}

const useStyles = createUseStyles({
  root: {
    padding: [35, 50],
    fontFamily: 'Inter, sans-serif',
  },
  heading: {
    display: 'flex',
    alignItems: 'center',
    gap: 20,
  },
  title: {
    fontWeight: 500,
  },
  table: {
    marginTop: 40,
    fontFamily: 'Inter, sans-serif',
  },
  tableHeading: {},
  tableHeadingCell: {
    borderRight: '3px solid white',
    backgroundColor: 'rgba(248, 248, 248, 1)',
    fontSize: 14,
    fontWeight: 400,
    padding: [10, 14],
    maxWidth: 240,
    textAlign: 'center',
  },
  tableRow: {
    // '& :hover': {
    //   backgroundColor: 'rgba(230, 245, 247, 1)',
    // },
  },
  tableCell: {
    borderRight: '3px solid white',
    fontSize: 14,
    fontWeight: 400,
    textAlign: 'center',
    padding: 10,
  },
  vacation: {
    backgroundColor: 'rgba(255, 236, 222, 1)',
  },
  work: {
    backgroundColor: 'rgba(230, 245, 247, 1)',
  },
  sickness: {
    backgroundColor: 'rgba(255, 226, 226, 1)',
  },
})
