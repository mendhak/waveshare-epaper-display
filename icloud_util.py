import datetime
import logging
import os
import re
import typing as T

import caldav

import caldav_util
from utility import configure_logging

configure_logging()

icloud_username = os.getenv("ICLOUD_USERNAME", None)
icloud_password = os.getenv("ICLOUD_APPLICATION_SPECIFIC_PASSWORD", None)


def get_auth_dict() -> dict:
    return {'username': icloud_username, 'password': icloud_password}


def get_icloud_calendar_events(calendar_id, from_date, to_date, username=None, password=None) -> T.List[caldav.Event]:
    caldav_url = "https://caldav.icloud.com/"
    return caldav_util.get_caldav_calendar_events(caldav_url, calendar_id, from_date, to_date, username, password)


def parse_icloud_calendar_url_into_id(url):
    m = re.search(r"https://.*\.icloud.com.*/.*/calendars/(.*)/", str(url))
    if m:
        return m.group(1)
    else:
        return str(url)


def get_icloud_datetime_formatted(event):
    return caldav_util.get_caldav_datetime_formatted(event)


def main():
    auth_dict = get_auth_dict()

    caldav_url = "https://caldav.icloud.com/"

    if auth_dict:
        with caldav.DAVClient(url=caldav_url, **auth_dict) as client:
            my_principal = client.principal()
            calendars = my_principal.calendars()

        print("")
        print("Here are the available Calendar names and IDs.  Copy the ID of the Calendar you want into env.sh")
        for cal in calendars:
            cal_id = parse_icloud_calendar_url_into_id(cal.url)
            print("============================================")
            print("Name               : ", cal.name)
            print("ID                 : ", parse_icloud_calendar_url_into_id(cal.url))
            print("URL                : ", cal.url)
            print("Any upcoming events: ")
            now = datetime.datetime.now().astimezone().replace(microsecond=0)
            oneyearlater = (
                    datetime.datetime.now().astimezone() + datetime.timedelta(days=365)).astimezone()
            logging.debug(now)
            logging.debug(oneyearlater)
            events_data = get_icloud_calendar_events(cal_id, now, oneyearlater, **auth_dict)

            for event in events_data:
                print("     ", event.vobject_instance.vevent.summary.value, ": ", get_icloud_datetime_formatted(event))
            print("============================================")


if __name__ == "__main__":
    main()
