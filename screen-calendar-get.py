import datetime
import os.path
import os
import logging
from calendar_providers.base_provider import CalendarEvent
from calendar_providers.caldav import CalDavCalendar
from calendar_providers.google import GoogleCalendar
from calendar_providers.ics import ICSCalendar
from calendar_providers.outlook import OutlookCalendar
from utility import get_formatted_time, update_svg, configure_logging, get_formatted_date, configure_locale

configure_locale()
configure_logging()

# note: increasing this will require updates to the SVG template to accommodate more events
max_event_results = 10

google_calendar_id = os.getenv("GOOGLE_CALENDAR_ID", "primary")
outlook_calendar_id = os.getenv("OUTLOOK_CALENDAR_ID", None)

caldav_calendar_url = os.getenv('CALDAV_CALENDAR_URL', None)
caldav_username = os.getenv("CALDAV_USERNAME", None)
caldav_password = os.getenv("CALDAV_PASSWORD", None)
caldav_calendar_id = os.getenv("CALDAV_CALENDAR_ID", None)

ics_calendar_url = os.getenv("ICS_CALENDAR_URL", None)

ttl = float(os.getenv("CALENDAR_TTL", 1 * 60 * 60))


def get_formatted_calendar_events(fetched_events: list[CalendarEvent]) -> dict:
    formatted_events = {}
    event_count = len(fetched_events)

    for index in range(max_event_results):
        event_label_id = str(index + 1)
        if index <= event_count - 1:
            formatted_events['CAL_DATETIME_' + event_label_id] = get_datetime_formatted(fetched_events[index].start, fetched_events[index].end, fetched_events[index].all_day_event)
            formatted_events['CAL_DESC_' + event_label_id] = fetched_events[index].summary
        else:
            formatted_events['CAL_DATETIME_' + event_label_id] = ""
            formatted_events['CAL_DESC_' + event_label_id] = ""

    return formatted_events


def get_datetime_formatted(event_start, event_end, is_all_day_event):

    if is_all_day_event or type(event_start) == datetime.date:
        start = datetime.datetime.combine(event_start, datetime.time.min)
        end = datetime.datetime.combine(event_end, datetime.time.min)

        start_day = get_formatted_date(start, include_time=False)
        end_day = get_formatted_date(end, include_time=False)
        if start == end:
            day = start_day
        else:
            day = "{} - {}".format(start_day, end_day)
    elif type(event_start) == datetime.datetime:
        start_date = event_start
        end_date = event_end
        if start_date.date() == end_date.date():
            start_formatted = get_formatted_date(start_date)
            end_formatted = get_formatted_time(end_date)
        else:
            start_formatted = get_formatted_date(start_date)
            end_formatted = get_formatted_date(end_date)
        day = "{} - {}".format(start_formatted, end_formatted)
    else:
        day = ''
    return day


def main():

    output_svg_filename = 'screen-output-weather.svg'

    today_start_time = datetime.datetime.utcnow()
    if os.getenv("CALENDAR_INCLUDE_PAST_EVENTS_FOR_TODAY", "0") == "1":
        today_start_time = datetime.datetime.combine(datetime.datetime.utcnow(), datetime.datetime.min.time())
    oneyearlater_iso = (datetime.datetime.now().astimezone()
                        + datetime.timedelta(days=365)).astimezone()

    if outlook_calendar_id:
        logging.info("Fetching Outlook Calendar Events")
        provider = OutlookCalendar(outlook_calendar_id, max_event_results, today_start_time, oneyearlater_iso)
    elif caldav_calendar_url:
        logging.info("Fetching Caldav Calendar Events")
        provider = CalDavCalendar(caldav_calendar_url, caldav_calendar_id, max_event_results,
                                  today_start_time, oneyearlater_iso, caldav_username, caldav_password)
    elif ics_calendar_url:
        logging.info("Fetching ics Calendar Events")
        provider = ICSCalendar(ics_calendar_url, max_event_results, today_start_time, oneyearlater_iso)
    else:
        logging.info("Fetching Google Calendar Events")
        provider = GoogleCalendar(google_calendar_id, max_event_results, today_start_time, oneyearlater_iso)

    calendar_events = provider.get_calendar_events()
    output_dict = get_formatted_calendar_events(calendar_events)

    logging.info("main() - {}".format(output_dict))

    logging.info("Updating SVG")
    update_svg(output_svg_filename, output_svg_filename, output_dict)


if __name__ == "__main__":
    main()
