import datetime
import logging
import emoji
import tomllib
import pickle
from xml.sax.saxutils import escape
from calendar_providers.base_provider import CalendarEvent
from calendar_providers.caldav import CalDavCalendar
from calendar_providers.google import GoogleCalendar
from calendar_providers.ics import ICSCalendar
from calendar_providers.outlook import OutlookCalendar
from utility import get_formatted_time, update_svg, configure_logging, get_formatted_date, configure_locale, is_stale

with open("config.toml", "rb") as f:
    config = tomllib.load(f)

configure_locale()
configure_logging(config["locale"]["log_level"])

calendar_config = config["calendar"]
max_event_results = calendar_config["max_events"]
ttl = float(calendar_config["cache_ttl_seconds"])
include_past_events_for_today = calendar_config.get("include_past_events_for_today", False)

# arrays of calendars
providers = calendar_config.get("providers", {})
google_calendars = providers.get("google", [])
outlook_calendars = providers.get("outlook", [])
ics_calendars = providers.get("ics", [])
caldav_calendars = providers.get("caldav", [])


def get_formatted_calendar_events(fetched_events: list[CalendarEvent]) -> dict:
    formatted_events = {}
    event_count = len(fetched_events)

    for index in range(max_event_results):
        event_label_id = str(index + 1)
        if index <= event_count - 1:
            formatted_events['CAL_DATETIME_' + event_label_id] = get_datetime_formatted(fetched_events[index].start, fetched_events[index].end, fetched_events[index].all_day_event)
            formatted_events['CAL_DATETIME_START_' + event_label_id] = get_datetime_formatted(fetched_events[index].start, fetched_events[index].end, fetched_events[index].all_day_event, True)
            formatted_events['CAL_DESC_' + event_label_id] = fetched_events[index].summary
        else:
            formatted_events['CAL_DATETIME_' + event_label_id] = ""
            formatted_events['CAL_DESC_' + event_label_id] = ""

    return formatted_events


def get_datetime_formatted(event_start, event_end, is_all_day_event, start_only=False):

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
        day = start_formatted if start_only else "{} - {}".format(start_formatted, end_formatted)
    else:
        day = ''
    return day


def fetch_all_calendar_events():
    """Fetch events from all enabled calendar providers. No caching - always fetch fresh."""
    all_calendar_events = []

    today_start_time = datetime.datetime.now(datetime.UTC).replace(tzinfo=None)
    if include_past_events_for_today:
        today_start_time = datetime.datetime.combine(datetime.datetime.now(datetime.UTC).date(), datetime.datetime.min.time())
    oneyearlater_iso = (datetime.datetime.now().astimezone()
                        + datetime.timedelta(days=365)).astimezone()

    for google_cal in google_calendars:
        if google_cal.get("enabled", True):
            calendar_id = google_cal.get("id", "primary")
            logging.info(f"Fetching Google Calendar: {calendar_id}")
            provider = GoogleCalendar(calendar_id, max_event_results, today_start_time, oneyearlater_iso)
            all_calendar_events.extend(provider.get_calendar_events())

    for outlook_cal in outlook_calendars:
        if outlook_cal.get("enabled", True):
            calendar_id = outlook_cal.get("calendar_id")
            logging.info(f"Fetching Outlook Calendar: {calendar_id}")
            provider = OutlookCalendar(calendar_id, max_event_results, today_start_time, oneyearlater_iso)
            all_calendar_events.extend(provider.get_calendar_events())

    for ics_cal in ics_calendars:
        if ics_cal.get("enabled", True):
            ics_url = ics_cal.get("url")
            logging.info(f"Fetching ICS Calendar: {ics_url}")
            provider = ICSCalendar(ics_url, max_event_results, today_start_time, oneyearlater_iso)
            all_calendar_events.extend(provider.get_calendar_events())

    for caldav_cal in caldav_calendars:
        if caldav_cal.get("enabled", True):
            caldav_url = caldav_cal.get("url")
            caldav_id = caldav_cal.get("id")
            caldav_user = caldav_cal.get("username")
            caldav_pass = caldav_cal.get("password")
            logging.info(f"Fetching CalDAV Calendar: {caldav_url}")
            provider = CalDavCalendar(caldav_url, caldav_id, max_event_results,
                                      today_start_time, oneyearlater_iso, caldav_user, caldav_pass)
            all_calendar_events.extend(provider.get_calendar_events())

    return all_calendar_events


def main():

    output_svg_filename = 'screen-output-weather.svg'
    cache_file = 'cache_all_calendars.pickle'

    if is_stale(cache_file, ttl):
        logging.info("Cache is stale, fetching fresh calendar data")
        all_calendar_events = fetch_all_calendar_events()

        with open(cache_file, 'wb') as f:
            pickle.dump(all_calendar_events, f)
        logging.info(f"Saved {len(all_calendar_events)} events to cache")
    else:
        logging.info("Using cached calendar data")
        with open(cache_file, 'rb') as f:
            all_calendar_events = pickle.load(f)

    logging.debug("All calendar events before normalization: {}".format(all_calendar_events))

    # convert tz-aware datetimes to local time, then make all naive for sorting
    from dateutil import tz as dateutil_tz
    normalized = []
    for event in all_calendar_events:
        start = event.start
        end = event.end
        if hasattr(start, 'tzinfo') and start.tzinfo is not None:
            start = start.astimezone(dateutil_tz.tzlocal()).replace(tzinfo=None)
        if hasattr(end, 'tzinfo') and end.tzinfo is not None:
            end = end.astimezone(dateutil_tz.tzlocal()).replace(tzinfo=None)
        normalized.append(CalendarEvent(event.summary, start, end, event.all_day_event))

    all_calendar_events = sorted(normalized, key=lambda x: x.start)
    calendar_events = all_calendar_events
    output_dict = get_formatted_calendar_events(calendar_events)

    # XML escape for safety
    for key, value in output_dict.items():
        output_dict[key] = escape(value)

    # Surround emojis with font-family emoji so it's rendered properly. Workaround for cairo not using fallback fonts.
    for key, value in output_dict.items():
        output_dict[key] = emoji.replace_emoji(value,  replace=lambda chars, data_dict: '<tspan style="font-family:emoji">' + chars + '</tspan>')

    logging.info("main() - {}".format(output_dict))

    logging.info("Updating SVG")
    update_svg(output_svg_filename, output_svg_filename, output_dict)


if __name__ == "__main__":
    main()
