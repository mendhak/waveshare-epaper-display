
import datetime
from calendar_providers.base_provider import BaseCalendarProvider, CalendarEvent
import logging
import pickle
import icalevents.icalevents
from dateutil import tz
from tzlocal import get_localzone


class ICSCalendar(BaseCalendarProvider):

    def __init__(self, ics_calendar_url, max_event_results, from_date, to_date):
        self.ics_calendar_url = ics_calendar_url
        self.max_event_results = max_event_results
        self.from_date = from_date
        self.to_date = to_date

    def get_calendar_events(self) -> list[CalendarEvent]:
        calendar_events = []

        logging.debug("Fetching ICS Calendar")

        ics_events = icalevents.icalevents.events(self.ics_calendar_url, start=self.from_date, end=self.to_date, tzinfo=get_localzone(), strict=True, sort=True)

        logging.debug(ics_events)

        for ics_event in ics_events[0:self.max_event_results]:
            event_start = ics_event.start
            event_end = ics_event.end

            # ICS Calendar marks the 'end' of all-day-events as
            # the day _after_ the last day. eg, Today's all day event ends tomorrow!
            # So subtract a day, if the event is an all day event
            if ics_event.all_day:
                event_end = event_end - datetime.timedelta(days=1)

            calendar_events.append(CalendarEvent(ics_event.summary, event_start, event_end, ics_event.all_day))

        return calendar_events
