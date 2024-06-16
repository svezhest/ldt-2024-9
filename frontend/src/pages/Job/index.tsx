import {Fragment, useEffect, useRef, useState} from 'react'
import {ButtonSlider} from '../../ui-kit/ButtonSlider'
import {createUseStyles} from 'react-jss'
import {getDoctor, getWorkloadByDoctor, postWorkloadByDoctor} from '../../api'
import {RootState} from '../../storage/store'
import {useSelector} from 'react-redux'
import {BlueButton, Loader} from '../../ui-kit'

export const Job = () => {
  const c = useStyles()
  const account = useSelector((state: RootState) => state.account)
  // const [skills, setSkills] = useState<null | Skills>(null)
  const skills = useRef<string[]>([])
  const [workloadInfo, setWorkloadInfo] = useState<{workload_type: string; amount: number}[]>([])
  const [isLoading, setLoading] = useState(true)

  useEffect(() => {
    if ((account.id || account.id === 0) && account.token) {
      getDoctor(account.id, account.token)
        .then((res) => {
          if (res.skills.primary_skill) {
            skills.current.push(res.skills.primary_skill)
          }
          if (res.skills.secondary_skills) {
            res.skills.secondary_skills.forEach((el) => {
              if (!skills.current.includes(el)) {
                skills.current.push(el)
              }
            })
          }
          return
        })
        .then(() => {
          if (account.id && account.token) {
            const workloadPromises = skills.current.map((el) => {
              return getWorkloadByDoctor(el, account.id ?? 0, account.token ?? '')
            })

            Promise.all(workloadPromises)
              .then((results) => {
                const newWorkloadInfo = results.map((el) => ({
                  workload_type: el.workload_type,
                  amount: el.amount,
                }))
                setWorkloadInfo(newWorkloadInfo)
              })
              .catch((error) => {
                // eslint-disable-next-line no-console
                console.error(error)
              })
              .then(() => {
                setLoading(false)
              })
          }
        })
    }
  }, [account.id, account.token])

  const postInfo = () => {
    const workloadPromises = workloadInfo.map((el) => {
      if (account.id && account.token) {
        return postWorkloadByDoctor(el.workload_type, account.id, el.amount, account.token)
      }
    })

    Promise.all(workloadPromises).then(() => {
      alert('Результат сохранен')
    })
  }

  return (
    <>
      {isLoading ? (
        <Loader />
      ) : (
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
                        <input
                          className={c.tableCellInput}
                          value={el.amount} // event.target.value)
                          onChange={(event) => {
                            const newWorkloadInfo = [...workloadInfo]
                            newWorkloadInfo[
                              workloadInfo.findIndex((workloadInfo) => workloadInfo.workload_type === el.workload_type)
                            ].amount = +event.target.value
                            setWorkloadInfo(newWorkloadInfo)
                          }}
                        />
                      </td>
                      <td className={c.tableCell}>{el.amount}</td>
                    </tr>
                  </Fragment>
                ))}
              </table>
              <BlueButton isInverse size='sm' text='Отправить' onClick={postInfo} className={c.button} />
            </div>
          </div>
        </div>
      )}
    </>
  )
}

const useStyles = createUseStyles({
  button: {
    marginTop: 40,
  },
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
