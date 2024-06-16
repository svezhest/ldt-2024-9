import {Fragment, useEffect, useRef, useState} from 'react'
import {ButtonSlider} from '../../ui-kit/ButtonSlider'
import {createUseStyles} from 'react-jss'
import {getDoctor, getWorkloadByDoctor} from '../../api'
import {RootState} from '../../storage/store'
import {useSelector} from 'react-redux'

export const Job = () => {
  const c = useStyles()
  const account = useSelector((state: RootState) => state.account)
  // const [skills, setSkills] = useState<null | Skills>(null)
  const skills = useRef<string[]>([])
  const [workloadInfo, setWorkloadInfo] = useState<{workload_type: string; amount: number}[]>([])

  useEffect(() => {
    // eslint-disable-next-line no-console
    console.log(account.id)
    if ((account.id || account.id === 0) && account.token) {
      getDoctor(account.id, account.token)
        .then((res) => {
          if (res.skills.primary_skill) {
            skills.current.push(res.skills.primary_skill)
          }
          if (res.skills.secondary_skills) {
            res.skills.secondary_skills.forEach((el) => {
              skills.current.push(el)
            })
          }
          return
        })
        .then(() => {
          skills.current.forEach((el) => {
            if (account.id && account.token) {
              // eslint-disable-next-line no-console
              console.log('workload_type:', el, 'doctor_id:', account.id, 'token;', account.token)
              getWorkloadByDoctor(el, account.id ?? 0, account.token ?? '').then((el) => {
                setWorkloadInfo([...workloadInfo, {workload_type: el.workload_type, amount: el.amount}])
                // eslint-disable-next-line no-console
                console.log(workloadInfo)
              })
            }
          })
        })
    }
  }, [account.id, account.token])

  return (
    <div className={c.root}>
      <h1 className={c.header}>Врач-рентгенолог</h1>
      <div className={c.content}>
        <p className={c.text}>Текущий рабочий статус</p>
        <ButtonSlider
          first={{isActive: false, onClick: () => null, text: 'на работе'}}
          second={{isActive: false, onClick: () => null, text: 'выходной'}}
          third={{isActive: false, onClick: () => () => null, text: 'в отпуске'}}
        />
        <div className={c.tableWrapper}>
          <p className={c.text}>Проведение исследований</p>
          <table className={c.table}>
            <tr className={c.tableHeading}>
              <td className={c.tableHeadingCell}>Тип</td>
              <td className={c.tableHeadingCell}>Сделано</td>
              <td className={c.tableHeadingCell}>Нужно сделать исследований (прогноз)</td>
            </tr>
            {workloadInfo.map((el, i) => (
              <Fragment key={i}>
                <tr className={c.tableRow}>
                  <td className={c.tableCell}>{el.workload_type}</td>
                  <td className={c.tableCell}>
                    <input className={c.tableCellInput} />
                  </td>
                  <td className={c.tableCell}>{el.amount}</td>
                </tr>
              </Fragment>
            ))}
          </table>
        </div>
      </div>
    </div>
  )
}

const useStyles = createUseStyles({
  root: {
    padding: [40, 50],
  },
  header: {
    fontFamily: 'Inter, sans-serif',
    fontSize: 28,
  },
  content: {
    marginTop: 40,
  },
  text: {
    fontFamily: 'Inter, sans-serif',
    fontSize: 14,
    marginBottom: 5,
  },
  tableWrapper: {
    marginTop: 20,
  },
  table: {
    marginTop: 15,
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
    padding: 5,
  },
  tableCellInput: {
    padding: [5, 20],
    borderRadius: 12,
    backgroundColor: 'rgba(248, 248, 248, 1)',
    border: '1px solid rgba(248, 248, 248, 1)',

    '&:focus': {
      border: '1px solid rgba(88, 179, 192, 1)',
      backgroundColor: 'white',
      outline: 'none',
    },
  },
})
