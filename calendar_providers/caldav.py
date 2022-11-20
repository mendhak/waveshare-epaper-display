
import pickle
import caldav
from utility import get_formatted_date, is_stale
import os
import logging
import datetime
from .base_provider import BaseCalendarProvider, CalendarEvent


ttl = float(os.getenv("CALENDAR_TTL", 1 * 60 * 60))

class CalDav(BaseCalendarProvider):

    def __init__(self, calendar_url, calendar_id, max_event_results, username=None, password=None):
        self.calendar_url = calendar_url
        self.calendar_id = calendar_id
        self.max_event_results = max_event_results
        self.username = username
        self.password = password

    def get_calendar_events(self):

        caldav_calendar_pickle = 'cache_caldav.pickle'
        calendar_events: list[CalendarEvent] = []

        if is_stale(os.getcwd() + "/" + caldav_calendar_pickle, ttl):
            logging.debug("Pickle is stale, fetching Caldav Calendar")

            now = datetime.datetime.now().astimezone().replace(microsecond=0)
            oneyearlater = (datetime.datetime.now().astimezone() + datetime.timedelta(days=365)).astimezone()

            with caldav.DAVClient(url=self.calendar_url, username=self.username, password=self.password) as client:
                my_principal = client.principal()

                calendar = my_principal.calendar(cal_id=self.calendar_id)
                event_results = calendar.date_search(start=now, end=oneyearlater, expand=True)
                events_data = []

                for result in event_results:
                    for component in result.icalendar_instance.subcomponents:
                        events_data.append(component)
                
            # Sort by start date. Since some are dates, and some are datetimes, a simple string sort works
            events_data.sort(key=lambda x: str(x['DTSTART'].dt))
            
            for event in events_data[0:self.max_event_results]:

                # If a dtend isn't included, calculate it from the duration
                if 'DTEND' in event:
                    event_end = event['DTEND'].dt
                if 'DURATION' in event:
                    event_end = event['DTSTART'].dt + event['DURATION'].dt

                all_day_event = False
                # CalDav Calendar marks the 'end' of all-day-events as
                # the day _after_ the last day. eg, Today's all day event ends tomorrow!
                # So subtract a day, if the event is an all day event
                if isinstance(event_end, datetime.date):
                    event_end = event_end - datetime.timedelta(days=1)
                    all_day_event = True
                    
                calendar_events.append(CalendarEvent(str(event['SUMMARY']), event['DTSTART'].dt, event_end, all_day_event))

            with open(caldav_calendar_pickle, 'wb') as cal:
                    pickle.dump(calendar_events, cal)

            return calendar_events                    
        else:
            logging.info("Found in cache")
            with open(caldav_calendar_pickle, 'rb') as cal:
                calendar_events = pickle.load(cal)
                return calendar_events