
import datetime
from calendar_providers.base_provider import BaseCalendarProvider, CalendarEvent
import logging
import icalevents.icalevents
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

        # icalevents library requires timezone-aware datetimes when processing ICS files
        # that contain timezone information, otherwise it throws naive/aware comparison errors
        local_tz = get_localzone()
        from_date = self.from_date if self.from_date.tzinfo else self.from_date.replace(tzinfo=local_tz)
        to_date = self.to_date if self.to_date.tzinfo else self.to_date.replace(tzinfo=local_tz)

        ics_events = icalevents.icalevents.events(self.ics_calendar_url, start=from_date, end=to_date, tzinfo=local_tz, strict=True, sort=True)

        logging.debug(ics_events)

        for ics_event in ics_events[0:self.max_event_results]:
            event_start = ics_event.start
            event_end = ics_event.end

            # ICS Calendar marks the 'end' of all-day-events as
            # the day _after_ the last day. eg, Today's all day event ends tomorrow!
            # So subtract a day, if the event is an all day event
            if ics_event.all_day:
                event_end = event_end - datetime.timedelta(days=1)

            # Normalize to naive datetime for consistent sorting
            if isinstance(event_start, datetime.date) and not isinstance(event_start, datetime.datetime):
                event_start = datetime.datetime.combine(event_start, datetime.time.min)
            elif isinstance(event_start, datetime.datetime) and event_start.tzinfo is not None:
                event_start = event_start.astimezone(local_tz).replace(tzinfo=None)

            if isinstance(event_end, datetime.date) and not isinstance(event_end, datetime.datetime):
                event_end = datetime.datetime.combine(event_end, datetime.time.min)
            elif isinstance(event_end, datetime.datetime) and event_end.tzinfo is not None:
                event_end = event_end.astimezone(local_tz).replace(tzinfo=None)

            calendar_events.append(CalendarEvent(ics_event.summary, event_start, event_end, ics_event.all_day))

        return calendar_events
