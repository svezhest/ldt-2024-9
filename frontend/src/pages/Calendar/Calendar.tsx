/* eslint-disable @typescript-eslint/no-non-null-assertion */
import React, {useState} from 'react'
import {Calendar, momentLocalizer, Views} from 'react-big-calendar'
import moment from 'moment'
import 'moment/locale/ru'
import 'react-big-calendar/lib/css/react-big-calendar.css'
import {createUseStyles} from 'react-jss'
import {ArrowLeft} from '../../ui-kit/ArrowLeft'
import classNames from 'classnames'

// Локализация для 'react-big-calendar' с использованием 'moment'
moment.locale('ru')
const localizer = momentLocalizer(moment)

const events = [
  {
    title: '13:00 - 18:00',
    start: new Date(2024, 5, 3, 13, 0, 0),
    end: new Date(2024, 5, 3, 18, 0, 0),
  },
  // Добавьте остальные события аналогичным образом
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
    marginBottom: 40,
  },
  title: {
    fontSize: '24px',
    fontWeight: 'bold',
    textTransform: 'capitalize',
    fontFamily: 'Inter, sans-serif',
  },
  buttonGroup: {
    display: 'flex',
    gap: 8,
    backgroundColor: 'rgba(248, 248, 248, 1)',
    padding: 8,
    borderRadius: 12,
  },
  activeButton: {
    backgroundColor: 'white !important',
  },
  button: {
    padding: [5, 12],
    fontSize: 12,
    border: 'none',
    borderRadius: 8,
    cursor: 'pointer',
    backgroundColor: 'transparent',
    '&:hover': {
      backgroundColor: 'white',
    },
    '&:active': {
      backgroundColor: 'white',
    },
  },
  leftHeader: {
    display: 'flex',
    alignItems: 'center',
    gap: 26,
  },
  crosses: {
    display: 'flex',
    gap: 10,
  },
  arrow: {
    backgroundColor: 'rgba(248, 248, 248, 1)',
    borderRadius: 12,
    padding: 6,
    cursor: 'pointer',
    '&:active': {
      backgroundColor: 'white',
    },
  },
  rotate: {
    transform: 'rotate(180deg)',
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
      padding: '5px',
      backgroundColor: 'transparent',
    },
    '& .rbc-today': {
      backgroundColor: '#e0e0e0',
    },
    '& .rbc-day-bg': {
      backgroundColor: 'white',
      border: 'none',
    },
    '& .rbc-month-row': {
      border: 'none',
    },
    '& .rbc-month-header': {
      display: 'none',
    },
    '& .rbc-button-link': {
      fontSize: 14,
      fontWeight: 600,
      fontFamily: 'Inter, sans-serif',
    },
    '& .rbc-event-content': {
      fontSize: 14,
      fontWeight: 500,
      fontFamily: 'Inter, sans-serif',
      color: 'black',
      textAlign: 'center',
    },
    '& .rbc-row-segment': {
      marginTop: 10,
      borderRadius: 10,
      backgroundColor: 'rgba(224, 224, 224, 0.2)',
      padding: [10, 24],
    },
    '& .rbc-toolbar': {
      display: 'none',
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
          <div className={classes.crosses}>
            <button className={classes.arrow} onClick={() => handleNavigate('PREV')}>
              <ArrowLeft />
            </button>
            <button className={classNames(classes.arrow, classes.rotate)} onClick={() => handleNavigate('NEXT')}>
              <ArrowLeft />
            </button>
          </div>
        </div>
        <div className={classes.buttonGroup}>
          <button
            className={`${classes.button} ${String(view) === 'day' ? classes.activeButton : undefined}`}
            onClick={() => handleViewChange(Views.DAY)}
          >
            День
          </button>
          <button
            className={`${classes.button} ${String(view) === 'week' ? classes.activeButton : undefined}`}
            onClick={() => handleViewChange(Views.WEEK)}
          >
            Неделя
          </button>
          <button
            className={`${classes.button} ${String(view) === 'month' ? classes.activeButton : undefined}`}
            onClick={() => handleViewChange(Views.MONTH)}
          >
            Месяц
          </button>
        </div>
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
        style={{height: 800}}
      />
    </div>
  )
}

export default MyCalendar
