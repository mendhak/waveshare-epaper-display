import datetime
import html
import time
import pickle
import os.path
import os
import logging

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from utility import is_stale, update_svg

logging.root.setLevel(logging.INFO)

# note: increasing this will require updates to the SVG template to accommodate more events
max_event_results = 4

google_calendar_id=os.getenv("GOOGLE_CALENDAR_ID","primary")
ttl = float(os.getenv("CALENDAR_TTL", 1 * 60 * 60))

def get_google_credentials():

    google_token_pickle = 'token.pickle'
    google_credentials_json = 'credentials.json'
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
            flow = InstalledAppFlow.from_client_secrets_file(
                google_credentials_json, google_api_scopes)
            credentials = flow.run_local_server()
        # Save the credentials for the next run
        with open(google_token_pickle, 'wb') as token:
            pickle.dump(credentials, token)

    return credentials


def get_google_events(max_event_results):

    google_calendar_pickle = 'calendar.pickle'

    service = build('calendar', 'v3', credentials=get_google_credentials(), cache_discovery=False)

    events_result = None

    if is_stale(os.getcwd() + "/" + google_calendar_pickle, ttl):
        logging.debug("Pickle is stale, calling the Calendar API")

        # Call the Calendar API
        events_result = service.events().list(
            calendarId=google_calendar_id, 
            timeMin=datetime.datetime.utcnow().isoformat() + 'Z',
            maxResults=max_event_results,
            singleEvents=True,
            orderBy='startTime').execute()

        with open(google_calendar_pickle, 'wb') as cal:
            pickle.dump(events_result, cal)

    else:
        logging.debug("Pickle is fresh, no need to call the Calendar API")
        with open(google_calendar_pickle,'rb') as cal:
            events_result = pickle.load(cal)

    events = events_result.get('items', [])

    if not events:
        logging.info("No upcoming events found.")

    return events


def get_output_dict_by_events(events, event_slot_count):
    formatted_events={}
    event_count = len(events)
    for event_i in range(event_slot_count):
        event_label_id = str(event_i + 1)
        if (event_i <= event_count - 1):
            formatted_events['CAL_DATETIME_' + event_label_id] = get_datetime_formatted(events[event_i]['start'])
            formatted_events['CAL_DESC_' + event_label_id] = events[event_i]['summary']
        else:
            formatted_events['CAL_DATETIME_' + event_label_id] = ""
            formatted_events['CAL_DESC_' + event_label_id] = ""
    return formatted_events


def get_datetime_formatted(event_start):
    if(event_start.get('dateTime')):
        start = event_start.get('dateTime')
        day = time.strftime("%a %b %-d, %-I:%M %p", time.strptime(start,"%Y-%m-%dT%H:%M:%S%z"))
    else:
        start = event_start.get('date')
        day = time.strftime("%a %b %-d", time.strptime(start, "%Y-%m-%d"))
    return day

def main():

    output_svg_filename = 'screen-output-weather.svg'

    google_events = get_google_events(max_event_results)
    output_dict = get_output_dict_by_events(google_events, max_event_results)

    logging.debug("main() - {}".format(output_dict))

    logging.info("Updating SVG")
    update_svg(output_svg_filename, output_svg_filename, output_dict)


if __name__ == "__main__":
    main()
