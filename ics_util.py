import icalendar
import requests
import datetime
from dateutil import tz
import logging
import pytz

def get_ics_calendar_events(ics_calendar_url, from_date: datetime.datetime, to_date: datetime.datetime):
    response = requests.get(ics_calendar_url)
    calendar = icalendar.cal.Calendar.from_ical(response.content)
    all_events_data = (subcomponent for subcomponent in calendar.subcomponents if isinstance(subcomponent, icalendar.Event))
    events_data = []
    for event in all_events_data:
        logging.info(event)
        dtstart = event['DTSTART'].dt

        if isinstance(dtstart, datetime.datetime): 
            if from_date.astimezone(pytz.utc) < dtstart.astimezone(pytz.utc) < to_date.astimezone(pytz.utc):
                events_data.append(event)
        elif isinstance(dtstart, datetime.date): 
            if from_date.date() < dtstart < to_date.date():
                events_data.append(event)

    return events_data
