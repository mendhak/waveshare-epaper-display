import sys
import json
import logging
import datetime
import requests
import msal
import atexit
import os


logging.basicConfig(level=logging.INFO)
logging.getLogger("msal").setLevel(logging.INFO)  # Optionally disable MSAL DEBUG logs

mscache = msal.SerializableTokenCache()
if os.path.exists("outlooktoken.bin"):
    mscache.deserialize(open("outlooktoken.bin", "r").read())

atexit.register(lambda:
    open("outlooktoken.bin", "w").write(mscache.serialize())
    if mscache.has_state_changed else None
    )

app = msal.PublicClientApplication("3b49f0d7-201a-4b5d-b2b4-8f4c3e6c8a30", authority="https://login.microsoftonline.com/consumers", token_cache=mscache)

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

    print(flow["message"])
    sys.stdout.flush()  

    print("Getting token...")
    result = app.acquire_token_by_device_flow(flow)  


endpoint_calendar_view="https://graph.microsoft.com/v1.0/me/calendars/{0}/calendarview?startdatetime={1}&enddatetime={2}&$orderby=start/dateTime&$top=5"
endpoint_calendar_list="https://graph.microsoft.com/v1.0/me/calendars"

if "access_token" in result:

    headers={'Authorization': 'Bearer ' + result['access_token']}

    calendars_data = requests.get(endpoint_calendar_list, headers=headers).json()

    print("Here are the available Calendar names and IDs.  Copy the ID of the Calendar you want into env.sh")
    for cal in calendars_data["value"]:
        print("============================================")
        print("Name               : ", cal["name"])
        print("ID                 : ", cal["id"])
        print("Any upcoming events: ")
        now_iso = datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()
        oneyearlater_iso = (datetime.datetime.now().astimezone() + datetime.timedelta(days=365)).astimezone().isoformat()
        logging.debug(now_iso)
        logging.debug(oneyearlater_iso)
        events_data = requests.get(endpoint_calendar_view.format(cal["id"], requests.utils.quote(now_iso), requests.utils.quote(oneyearlater_iso)), headers=headers).json()
        for event in events_data["value"]:
            print("     ", event["subject"], ": ", event["start"]["dateTime"])
        print("============================================")



else:
    logging.error(result.get("error"))
    logging.error(result.get("error_description"))
    logging.error(result.get("correlation_id"))
