import caldav

import datetime
from utility import configure_logging, get_formatted_date
import typing as T
import os
import logging

configure_logging()

caldav_username = os.getenv("CALDAV_USERNAME", None)
caldav_password = os.getenv("CALDAV_PASSWORD", None)
caldav_url = os.getenv('CALDAV_CALENDAR_URL', None)


def get_auth_dict() -> dict:
    return {'username': caldav_username, 'password': caldav_password}


def get_caldav_calendar_events(calendar_url,
                               calendar_id,
                               from_date,
                               to_date,
                               max_event_results,
                               username=None, password=None) -> T.List[caldav.Event]:
    with caldav.DAVClient(url=calendar_url, username=username, password=password) as client:
        my_principal = client.principal()

        calendar = my_principal.calendar(cal_id=calendar_id)
        event_results = calendar.date_search(start=from_date, end=to_date, expand=True)
        events_data = []

        for result in event_results:
            for component in result.icalendar_instance.subcomponents:
                events_data.append(component)
        

    events_data.sort(key=lambda x: str(x['DTSTART'].dt))
    return events_data[0:max_event_results]


def get_caldav_datetime_formatted(event):
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


def main():
    auth_dict = get_auth_dict()
    if auth_dict:
        with caldav.DAVClient(url=caldav_url, **auth_dict) as client:
            my_principal = client.principal()
            calendars = my_principal.calendars()

        print("")
        print("Here are the available Calendar names and IDs.  Copy the ID of the Calendar you want into env.sh")
        for cal in calendars:
            print("============================================")
            print("Name               : ", cal.name)
            print("ID                 : ", cal.id)
            print("URL                 : ", cal.url)
            print("Any upcoming events: ")
            now = datetime.datetime.now().astimezone().replace(microsecond=0)
            oneyearlater = (
                    datetime.datetime.now().astimezone() + datetime.timedelta(days=365)).astimezone()
            logging.debug(now)
            logging.debug(oneyearlater)
            events_data = get_caldav_calendar_events(caldav_url, cal.id, now, oneyearlater, 50, **auth_dict)

            for event in events_data:
                print("     ", str(event['SUMMARY']), ": ", get_caldav_datetime_formatted(event))
            print("============================================")


if __name__ == "__main__":
    main()