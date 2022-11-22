
import datetime
from calendar_providers.base_provider import BaseCalendarProvider, CalendarEvent
from utility import is_stale
import os
import logging
import pickle
import msal
import requests
import sys
import json
from dateutil import tz

ttl = float(os.getenv("CALENDAR_TTL", 1 * 60 * 60))


class OutlookCalendar(BaseCalendarProvider):

    def __init__(self, outlook_calendar_id, max_event_results, from_date, to_date):
        self.max_event_results = max_event_results
        self.from_date = from_date
        self.to_date = to_date
        self.outlook_calendar_id = outlook_calendar_id

    def get_access_token(self):
        mscache = msal.SerializableTokenCache()
        if os.path.exists("outlooktoken.bin"):
            mscache.deserialize(open("outlooktoken.bin", "r").read())

        app = msal.PublicClientApplication("3b49f0d7-201a-4b5d-b2b4-8f4c3e6c8a30",
                                           authority="https://login.microsoftonline.com/consumers",
                                           token_cache=mscache)

        result = None

        accounts = app.get_accounts()

        if accounts:
            chosen = accounts[0]
            result = app.acquire_token_silent(["https://graph.microsoft.com/Calendars.Read"], account=chosen)

        if not result:
            logging.info("No token exists in cache, login is required.")

            flow = app.initiate_device_flow(scopes=["https://graph.microsoft.com/Calendars.Read"])
            if "user_code" not in flow:
                raise ValueError(
                    "Fail to create device flow. Err: %s" % json.dumps(flow, indent=4))

            print("")
            print(flow["message"])
            sys.stdout.flush()

            result = app.acquire_token_by_device_flow(flow)

        logging.debug(result)

        if "access_token" in result:
            if mscache.has_state_changed:
                open("outlooktoken.bin", "w").write(mscache.serialize())

            return result["access_token"]
        else:
            logging.error(result.get("error"))
            logging.error(result.get("error_description"))
            logging.error(result.get("correlation_id"))
            raise Exception(result.get("error"))

    def get_outlook_calendar_events(self, calendar_id, from_date, to_date, access_token):

        from_date_iso = from_date.replace(microsecond=0).isoformat()
        to_date_iso = to_date.isoformat()

        headers = {'Authorization': 'Bearer ' + access_token}
        endpoint_calendar_view = \
            "https://graph.microsoft.com/v1.0/me/calendars/{0}/calendarview?startdatetime={1}&enddatetime={2}&$orderby=start/dateTime&$top={3}"
        events_data = requests.get(
                                  endpoint_calendar_view.format(calendar_id,
                                                                requests.utils.quote(from_date_iso),
                                                                requests.utils.quote(to_date_iso),
                                                                self.max_event_results),
                                  headers=headers).json()
        return events_data

    def get_calendar_events(self, bypass_cache=False) -> list[CalendarEvent]:
        calendar_events = []
        outlook_calendar_pickle = 'cache_outlookcalendar.pickle'
        if bypass_cache or is_stale(os.getcwd() + "/" + outlook_calendar_pickle, ttl):
            logging.debug("Cache is stale, calling the Outlook Calendar API")

            access_token = self.get_access_token()
            events_data = self.get_outlook_calendar_events(
                self.outlook_calendar_id,
                self.from_date,
                self.to_date,
                access_token)
            logging.debug(events_data)

            if not bypass_cache:
                with open(outlook_calendar_pickle, 'wb') as cal:
                    pickle.dump(events_data, cal)
        else:
            logging.info("Found in cache")
            with open(outlook_calendar_pickle, 'rb') as cal:
                events_data = pickle.load(cal)

        for event in events_data["value"]:
            start_date = datetime.datetime.strptime(event["start"]["dateTime"], "%Y-%m-%dT%H:%M:%S.0000000")
            end_date = datetime.datetime.strptime(event["end"]["dateTime"], "%Y-%m-%dT%H:%M:%S.0000000")

            summary = event["subject"]
            is_all_day = event['isAllDay']

            # Outlook Calendar marks the 'end' of all-day-events as
            # the day _after_ the last day. eg, Today's all day event ends tomorrow midnight.
            # So subtract a day
            if is_all_day:
                end_date = end_date - datetime.timedelta(days=1)
            else:
                # Convert start/end to local time
                start_date = start_date.replace(tzinfo=tz.tzutc())
                start_date = start_date.astimezone(tz.tzlocal())
                end_date = end_date.replace(tzinfo=tz.tzutc())
                end_date = end_date.astimezone(tz.tzlocal())

            calendar_events.append(CalendarEvent(summary, start_date, end_date, is_all_day))

        return calendar_events
