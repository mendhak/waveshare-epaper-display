import icalendar
from icalevnt.icalevents import events
import requests
import datetime
from dateutil import tz
import logging
import pytz

def get_ics_calendar_events(ics_calendar_url, from_date: datetime.datetime, to_date: datetime.datetime, max_event_results):
    cal_events  = events(ics_calendar_url, start=from_date, end=to_date)
    cal_events.sort(key=lambda x: x.start)
    return cal_events[0:max_event_results]


