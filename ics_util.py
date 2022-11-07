import icalendar
import requests
import datetime


def get_ics_calendar_events(ics_calendar_url, from_date: datetime.datetime, to_date: datetime.datetime):
    response = requests.get(ics_calendar_url)
    calendar = icalendar.cal.Calendar.from_ical(response.content)
    all_events_data = (subcomponent for subcomponent in calendar.subcomponents if isinstance(subcomponent, icalendar.Event))
    events_data = []
    for event in all_events_data:
        dtstart = event['DTSTART'].dt
        if isinstance(dtstart, datetime.datetime) and from_date < dtstart < to_date:
            events_data.append(event)
        elif isinstance(dtstart, datetime.date) and from_date.date() < dtstart < to_date.date():
            events_data.append(event)

    return events_data
