/* eslint-disable @typescript-eslint/no-non-null-assertion */
import React, {useState} from 'react'
import {Calendar, momentLocalizer, Views} from 'react-big-calendar'
import moment from 'moment'
import 'moment/locale/ru'
import 'react-big-calendar/lib/css/react-big-calendar.css'
import {createUseStyles} from 'react-jss'
import {ButtonSlider, Arrows} from '../../ui-kit'

// Локализация для 'react-big-calendar' с использованием 'moment'
moment.locale('ru')
const localizer = momentLocalizer(moment)

const events = [
  {
    title: '13:00 - 18:00',
    start: new Date(2024, 5, 3, 13, 0, 0),
    end: new Date(2024, 5, 3, 18, 0, 0),
  },
  // Добавьте остальные события аналогичным образомx
]

const useStyles = createUseStyles({
  calendarContainer: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    padding: '20px',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    width: '100%',
    marginBottom: 10,
  },
  title: {
    fontSize: '24px',
    fontWeight: 'bold',
    textTransform: 'capitalize',
    fontFamily: 'Inter, sans-serif',
  },
  leftHeader: {
    display: 'flex',
    alignItems: 'center',
    gap: 26,
  },
  calendar: {
    width: '100%',
    '& .rbc-month-view': {
      border: 'none',
    },
    '& .rbc-header': {
      textAlign: 'center',
    },
    '& .rbc-event': {
      borderRadius: '5px',
      backgroundColor: 'transparent',
      padding: 0,
      display: 'flex',
      justifyContent: 'center',
    },
    '& .rbc-today': {
      backgroundColor: '#e0e0e0',
    },
    '& .rbc-day-bg': {
      backgroundColor: 'white',
      border: 'none',
      boxShadow: '0px 0px 10px 0px rgba(0,0,0,0.1)',
      margin: 5,
      borderRadius: 12,
    },
    '& .rbc-month-row': {
      border: 'none',
      marginTop: 5,
    },
    '& .rbc-month-header': {
      display: 'none',
    },
    '& .rbc-button-link': {
      fontSize: 14,
      fontWeight: 600,
      fontFamily: 'Inter, sans-serif',
      margin: 15,
    },
    '& .rbc-event-content': {
      fontSize: 14,
      fontWeight: 500,
      fontFamily: 'Inter, sans-serif',
      color: 'black',
      textAlign: 'center',
      backgroundColor: 'rgba(224, 224, 224, 0.2)',
      width: 'fit-content',
      padding: [10, 24],
      borderRadius: 10,
    },
    '& .rbc-row-segment': {
      marginTop: 10,
      borderRadius: 10,
      padding: 0,
      backgroundColor: 'transparent',
    },
    '& .rbc-toolbar': {
      display: 'none',
    },
    '& .rbc-row-bg': {
      gap: 5,
    },
  },
})

const MyCalendar = () => {
  const classes = useStyles()
  const [view, setView] = useState(Views.MONTH)
  const [currentDate, setCurrentDate] = useState(moment().toDate())

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const handleViewChange = (newView: any) => {
    setView(newView)
  }

  const handleNavigate = (action: 'PREV' | 'NEXT') => {
    let newDate
    if (action === 'PREV') {
      newDate = moment(currentDate).subtract(1, 'months').toDate()
    } else {
      newDate = moment(currentDate).add(1, 'months').toDate()
    }
    setCurrentDate(newDate)
  }

  return (
    <div className={classes.calendarContainer}>
      <div className={classes.header}>
        <div className={classes.leftHeader}>
          <h1 className={classes.title}>{moment(currentDate).format('MMMM YYYY')}</h1>
          <Arrows leftFunc={() => handleNavigate('PREV')} rightFunc={() => handleNavigate('NEXT')} />
        </div>
        <ButtonSlider
          first={{isActive: String(view) === 'day', onClick: () => handleViewChange(Views.DAY), text: 'День'}}
          second={{isActive: String(view) === 'week', onClick: () => handleViewChange(Views.WEEK), text: 'Неделя'}}
          third={{isActive: String(view) === 'month', onClick: () => handleViewChange(Views.MONTH), text: 'Месяц'}}
        />
      </div>
      <Calendar
        localizer={localizer}
        events={events}
        startAccessor='start'
        endAccessor='end'
        date={currentDate}
        view={view}
        views={[Views.MONTH, Views.WEEK, Views.DAY]}
        onNavigate={(date) => setCurrentDate(date)}
        onView={handleViewChange}
        className={classes.calendar}
        formats={{
          monthHeaderFormat: 'MMMM YYYY',
          weekdayFormat: (date, culture, localizer) => localizer!.format(date, 'dd', culture),
          dayFormat: (date, culture, localizer) => localizer!.format(date, 'D', culture),
        }}
        messages={{
          month: 'Месяц',
          week: 'Неделя',
          day: 'День',
          today: 'Сегодня',
          previous: 'Предыдущий',
          next: 'Следующий',
        }}
        style={{height: 700}}
      />
    </div>
  )
}

export default MyCalendar
