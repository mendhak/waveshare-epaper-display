import datetime
from calendar_providers.base_provider import BaseCalendarProvider, CalendarEvent
from utility import is_stale, xor_decode
import os
import logging
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

ttl = float(os.getenv("CALENDAR_TTL", 1 * 60 * 60))
google_calendar_timezone = os.getenv("GOOGLE_CALENDAR_TIME_ZONE_NAME", None)


class GoogleCalendar(BaseCalendarProvider):
    def __init__(self, google_calendar_id, max_event_results, from_date, to_date):
        self.max_event_results = max_event_results
        self.from_date = from_date
        self.to_date = to_date
        self.google_calendar_id = google_calendar_id

    def get_google_credentials(self):

        google_token_pickle = 'token.pickle'

        google_api_scopes = ['https://www.googleapis.com/auth/calendar.readonly']

        credentials = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(google_token_pickle):
            with open(google_token_pickle, 'rb') as token:
                credentials = pickle.load(token)

        # If there are no (valid) credentials available, let the user log in.
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_config({"installed": {
                    "client_id": "872428123454-jjp9mvs2ha4at913874ik2ua6fosi23d.apps.googleusercontent.com",
                    "project_id": "waveshare-epaper-display",
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_secret": xor_decode("HwI5FzprZiBiE0AtJ3A7IjZ+LB4VCBQjHmcIN1IBJz0QBjg=", "XMzDj3Kb4j2j_3jK_8dwoeuir3mm3jKb"),
                    "redirect_uris": ["http://localhost"]}}, google_api_scopes)

                credentials = flow.run_local_server()
            # Save the credentials for the next run
            with open(google_token_pickle, 'wb') as token:
                pickle.dump(credentials, token)

        return credentials

    def get_calendar_events(self) -> list[CalendarEvent]:
        calendar_events = []
        google_calendar_pickle = 'cache_calendar.pickle'

        service = build('calendar', 'v3', credentials=self.get_google_credentials(), cache_discovery=False)

        events_result = None

        if is_stale(os.getcwd() + "/" + google_calendar_pickle, ttl):
            logging.debug("Pickle is stale, calling the Calendar API")

            # Call the Calendar API
            events_result = service.events().list(
                calendarId=self.google_calendar_id,
                timeMin=self.from_date.isoformat() + 'Z',
                timeZone=google_calendar_timezone,
                maxResults=self.max_event_results,
                singleEvents=True,
                orderBy='startTime').execute()

            for event in events_result.get('items', []):
                if event['start'].get('date'):
                    is_all_day = True
                    start_date = datetime.datetime.strptime(event['start'].get('date'), "%Y-%m-%d")
                    end_date = datetime.datetime.strptime(event['end'].get('date'), "%Y-%m-%d")
                    # Google Calendar marks the 'end' of all-day-events as
                    # the day _after_ the last day. eg, Today's all day event ends tomorrow!
                    # So subtract a day
                    end_date = end_date - datetime.timedelta(days=1)
                else:
                    is_all_day = False
                    start_date = datetime.datetime.strptime(event['start'].get('dateTime'), "%Y-%m-%dT%H:%M:%S%z")
                    end_date = datetime.datetime.strptime(event['end'].get('dateTime'), "%Y-%m-%dT%H:%M:%S%z")

                summary = event['summary']

                calendar_events.append(CalendarEvent(summary, start_date, end_date, is_all_day))

            with open(google_calendar_pickle, 'wb') as cal:
                pickle.dump(calendar_events, cal)

        else:
            logging.info("Found in cache")
            with open(google_calendar_pickle, 'rb') as cal:
                calendar_events = pickle.load(cal)

        if len(calendar_events) == 0:
            logging.info("No upcoming events found.")

        return calendar_events
