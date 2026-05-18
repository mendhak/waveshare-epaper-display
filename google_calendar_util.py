import logging
import tomllib
import datetime
from utility import configure_logging
from googleapiclient.discovery import build
from calendar_providers.google import GoogleCalendar

with open("config.toml", "rb") as f:
    config = tomllib.load(f)

configure_logging(config.get("locale", {}).get("log_level", "INFO"))


def main():
    service = build('calendar', 'v3', credentials=GoogleCalendar.get_google_credentials(None), cache_discovery=False)
    calendars_list = service.calendarList().list().execute()

    print("")
    print("Here are the available Calendar names and IDs.  Copy the ID of the Calendar you want into config.toml")
    for calendar_list_entry in calendars_list['items']:
        print("============================================")
        print("Name: ", calendar_list_entry['summary'])
        print("ID  : ", calendar_list_entry['id'])
        print("Any upcoming events: ")
        upcoming_events = service.events().list(calendarId=calendar_list_entry['id'],
                                                timeMin=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                                                maxResults=10,
                                                singleEvents=True,
                                                orderBy='startTime').execute()
        for event in upcoming_events.get('items', [])[:5]:
            print(f'{event["summary"]}, {event["start"]}, {event["end"]}')
        print("============================================")


if __name__ == "__main__":
    logging.info("This is a utility script to help find the calendar ID for your Google Calendar")

    main()
