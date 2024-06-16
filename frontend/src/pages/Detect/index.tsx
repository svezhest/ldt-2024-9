import classNames from 'classnames'
import {Arrows, BlueButton, Loader} from '../../ui-kit'
import {createUseStyles} from 'react-jss'
import {useEffect, useState} from 'react'
import {getFile, getStats} from '../../api'
import {useSelector} from 'react-redux'
import {RootState} from '../../storage/store'
import {GetStats} from '../../api/types'

export const Detect = () => {
  const c = useStyles()
  const account = useSelector((state: RootState) => state.account)
  const [stats, setStats] = useState<GetStats | null>(null)
  const [isLoading, setLoading] = useState(true)

  useEffect(() => {
    if (account.token) {
      getStats(account.token)
        .then((res) => {
          // eslint-disable-next-line no-console
          console.log(res.stats)
          setStats(res.stats as unknown as GetStats)
          // eslint-disable-next-line no-console
          console.log(Array.isArray(stats), stats)
        })
        .finally(() => {
          setLoading(false)
        })
    }
  }, [account.token])

  return (
    <>
      {isLoading ? (
        <Loader />
      ) : (
        <div className={c.root}>
          <div className={c.heading}>
            <Arrows />
            <h2 className={c.title}>3.06 - 09.06</h2>
            <BlueButton
              isInverse
              text='Скачать отчет'
              onClick={() => {
                if (account.token) {
                  getFile(account.token).then((res) => {
                    // eslint-disable-next-line no-console
                    console.log(res)
                  })
                }
              }}
            />
          </div>
          <table className={c.table}>
            <tr className={c.tableHeading}>
              <td className={c.tableHeadingCell}>Тип</td>
              <td className={c.tableHeadingCell}>Сделано</td>
              <td className={c.tableHeadingCell}>Будет сделано за неделю (прогноз)</td>
              <td className={c.tableHeadingCell}>Нужно сделать исследований (прогноз)</td>
              <td className={c.tableHeadingCell}>Рекомендация</td>
            </tr>
            {Array.isArray(stats) &&
              stats.map((el, i) => (
                <tr
                  key={i}
                  className={classNames(
                    c.tableRow,
                    el.needed_prediction < el.done_prediction
                      ? c.work
                      : el.needed_prediction / 2 > el.done_prediction
                        ? c.sickness
                        : el.needed_prediction > el.done_prediction
                          ? c.vacation
                          : null
                  )}
                >
                  <td className={c.tableCell}>{el.workload_type}</td>
                  <td className={c.tableCell}>{el.done}</td>
                  <td className={c.tableCell}>{el.done_prediction}</td>
                  <td className={c.tableCell}>{el.needed_prediction}</td>
                  <td className={c.tableCell}>{el.recommendation}</td>
                </tr>
              ))}
          </table>
        </div>
      )}
    </>
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
