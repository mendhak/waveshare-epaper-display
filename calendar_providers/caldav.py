
import pickle
import caldav
from utility import get_formatted_date, is_stale
import typing as T
import os
import logging
import datetime
from calendar_providers.base_provider import BaseCalendarProvider

ttl = float(os.getenv("CALENDAR_TTL", 1 * 60 * 60))

class CalDav(BaseCalendarProvider):

    def __init__(self, calendar_url, calendar_id, max_event_results, username=None, password=None):
        self.calendar_url = calendar_url
        self.calendar_id = calendar_id
        self.max_event_results = max_event_results
        self.username = username
        self.password = password

    def get_caldav_datetime_formatted(self, event):
        event_start = event['DTSTART'].dt

        # If a dtend isn't included, calculate it from the duration
        if 'DTEND' in event:
            event_end = event['DTEND'].dt
        if 'DURATION' in event:
            event_end = event['DTSTART'].dt + event['DURATION'].dt

        if isinstance(event_start, datetime.datetime):
            start_date = event_start
            end_date = event_end
            if start_date.date() == end_date.date():
                start_formatted = get_formatted_date(start_date)
                end_formatted = end_date.strftime("%-I:%M %p")
            else:
                start_formatted = get_formatted_date(start_date)
                end_formatted = get_formatted_date(end_date)
            day = "{} - {}".format(start_formatted, end_formatted)
        elif isinstance(event_start, datetime.date):
            start = datetime.datetime.combine(event_start, datetime.time.min)
            end = datetime.datetime.combine(event_end, datetime.time.min)
            # CalDav Calendar marks the 'end' of all-day-events as
            # the day _after_ the last day. eg, Today's all day event ends tomorrow!
            # So subtract a day
            end = end - datetime.timedelta(days=1)
            start_day = get_formatted_date(start, include_time=False)
            end_day = get_formatted_date(end, include_time=False)
            if start == end:
                day = start_day
            else:
                day = "{} - {}".format(start_day, end_day)
        else:
            day = ''
        return day

    def get_calendar_events(self):

        caldav_calendar_pickle = 'cache_caldav.pickle'

        if is_stale(os.getcwd() + "/" + caldav_calendar_pickle, ttl):
            logging.debug("Pickle is stale, fetching Caldav Calendar")

            now = datetime.datetime.now().astimezone().replace(microsecond=0)
            oneyearlater = (
                    datetime.datetime.now().astimezone() + datetime.timedelta(days=365)).astimezone()

            with caldav.DAVClient(url=self.calendar_url, username=self.username, password=self.password) as client:
                my_principal = client.principal()

                calendar = my_principal.calendar(cal_id=self.calendar_id)
                event_results = calendar.date_search(start=now, end=oneyearlater, expand=True)
                events_data = []

                for result in event_results:
                    for component in result.icalendar_instance.subcomponents:
                        events_data.append(component)
                

            events_data.sort(key=lambda x: str(x['DTSTART'].dt))
            
            formatted_events = {}

            for index, event in enumerate(events_data[0:self.max_event_results]):
                event_label_id = str(index + 1)
                if index <= self.max_event_results - 1:
                    summary = str(event['SUMMARY'])
                    formatted_events['CAL_DATETIME_' + event_label_id] = self.get_caldav_datetime_formatted(event)
                    formatted_events['CAL_DESC_' + event_label_id] = summary
                else:
                    formatted_events['CAL_DATETIME_' + event_label_id] = ""
                    formatted_events['CAL_DESC_' + event_label_id] = ""

            # return events_data[0:self.max_event_results]
            with open(caldav_calendar_pickle, 'wb') as cal:
                    pickle.dump(formatted_events, cal)

            return formatted_events                    
        else:
            logging.info("Found in cache")
            with open(caldav_calendar_pickle, 'rb') as cal:
                formatted_events = pickle.load(cal)
                return formatted_events