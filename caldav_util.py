

import datetime
from calendar_providers.caldav import CalDavCalendar
from utility import configure_logging
import os

configure_logging()

caldav_username = os.getenv("CALDAV_USERNAME", None)
caldav_password = os.getenv("CALDAV_PASSWORD", None)
caldav_url = os.getenv('CALDAV_CALENDAR_URL', None)


def main():

    caldav = CalDavCalendar(caldav_url, None, 50, datetime.datetime.utcnow(),
                            (datetime.datetime.now().astimezone() + datetime.timedelta(days=365)).astimezone(),
                            caldav_username,
                            caldav_password)
    events = caldav.get_calendar_events()
    for event in events:
        print(f'{event.summary}, {event.start}, {event.end}')


if __name__ == "__main__":
    main()
