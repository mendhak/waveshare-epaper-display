import logging
import datetime
import requests
from calendar_providers.outlook import OutlookCalendar
from utility import configure_logging


configure_logging()


def main():

    access_token = OutlookCalendar(None, None, None, None).get_access_token()

    endpoint_calendar_list = "https://graph.microsoft.com/v1.0/me/calendars"

    if access_token:

        headers = {'Authorization': 'Bearer ' + access_token}

        calendars_data = requests.get(endpoint_calendar_list, headers=headers).json()

        print("")
        print("Here are the available Calendar names and IDs.  Copy the ID of the Calendar you want into env.sh")
        for cal in calendars_data["value"]:
            print("============================================")
            print("Name               : ", cal["name"])
            print("ID                 : ", cal["id"])
            print("Any upcoming events: ")

            today_start_time = datetime.datetime.utcnow()
            oneyearlater_iso = (datetime.datetime.now().astimezone() + datetime.timedelta(days=365)).astimezone()

            logging.debug(today_start_time)
            logging.debug(oneyearlater_iso)

            outlook_calendar = OutlookCalendar(cal["id"], 10, today_start_time, oneyearlater_iso)
            events_data = outlook_calendar.get_calendar_events(bypass_cache=True)

            for event in events_data:
                print(f'{event.summary}, {event.start}, {event.end}, {event.all_day_event}')
            print("============================================")


if __name__ == "__main__":
    main()
