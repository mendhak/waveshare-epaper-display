

import datetime
from calendar_providers.caldav import CalDav
from utility import configure_logging, get_formatted_date
import typing as T
import os
import logging

configure_logging()

caldav_username = os.getenv("CALDAV_USERNAME", None)
caldav_password = os.getenv("CALDAV_PASSWORD", None)
caldav_url = os.getenv('CALDAV_CALENDAR_URL', None)



def main():

    caldav = CalDav(caldav_url, None, 50, caldav_username, caldav_password)
    events = caldav.get_calendar_events()
    for event in events:
        print(event)


if __name__ == "__main__":
    main()
