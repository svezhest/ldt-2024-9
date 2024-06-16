import React, {useEffect} from 'react'
import MyCalendar from './Calendar'
import {getSchedule} from '../../api'
import {useSelector} from 'react-redux'
import {RootState} from '../../storage/store'

export const Calendar = () => {
  const account = useSelector((state: RootState) => state.account)

  useEffect(() => {
    if (account.id && account.token) {
      getSchedule(account.id, '2024-06-01', '2024-06-30', account.token).then((res) => {
        // eslint-disable-next-line no-console
        console.log(res)
        return
      })
    }
  }, [account.id, account.token])
  return <MyCalendar />
}
