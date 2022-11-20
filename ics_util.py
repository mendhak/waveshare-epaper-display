
import datetime
import os
from calendar_providers.ics import ICS

ics_calendar_url = os.getenv("ICS_CALENDAR_URL", None)


def main():
    ics = ICS(ics_calendar_url, 50, datetime.datetime.utcnow(),
              (datetime.datetime.now().astimezone() + datetime.timedelta(days=365)).astimezone())
    events = ics.get_calendar_events()
    for event in events:
        print(f'{event.summary}, {event.start}, {event.end}, {event.all_day_event}')


if __name__ == "__main__":
    main()
