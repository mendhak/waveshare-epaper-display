import sys
import json
import logging

import requests
import msal
import atexit
import os


logging.basicConfig(level=logging.INFO) 
# logging.getLogger("msal").setLevel(logging.INFO)  # Optionally disable MSAL DEBUG logs

mscache = msal.SerializableTokenCache()
if os.path.exists("mstoken.bin"):
    mscache.deserialize(open("mstoken.bin", "r").read())

atexit.register(lambda:
    open("mstoken.bin", "w").write(mscache.serialize())
    if mscache.has_state_changed else None
    )

app = msal.PublicClientApplication("3b49f0d7-201a-4b5d-b2b4-8f4c3e6c8a30", authority="https://login.microsoftonline.com/consumers", token_cache=mscache)

result = None

accounts = app.get_accounts()

if accounts:
    chosen = accounts[0]
    result = app.acquire_token_silent(["https://graph.microsoft.com/Calendars.Read"], account=chosen)

if not result:
    logging.info("No suitable token exists in cache. Let's get a new one from AAD.")

    flow = app.initiate_device_flow(scopes=["https://graph.microsoft.com/Calendars.Read"])
    if "user_code" not in flow:
        raise ValueError(
            "Fail to create device flow. Err: %s" % json.dumps(flow, indent=4))

    print(flow["message"])
    sys.stdout.flush()  

    print("Now acquire the token by device flow")
    result = app.acquire_token_by_device_flow(flow)  


endpoint_calendar_view="https://graph.microsoft.com/v1.0/me/calendars/AQMkADAwATM0MDAAMS1hYzNjLTlmZWQtMDACLTAwCgBGAAADOz8bO01f70e38Mnu6VwseAcAiqHWrA5pN0uypQeCv39hJAAAAgEGAAAAiqHWrA5pN0uypQeCv39hJAAEP3VdaAAAAA==/calendarView?startDateTime=2021-03-25T00:00:00Z&endDateTime=2021-04-25T00:00:00Z&$orderby=start/dateTime"
endpoint_calendar_list="https://graph.microsoft.com/v1.0/me/calendars"

if "access_token" in result:
    graph_data = requests.get(  
        endpoint_calendar_list,
        headers={'Authorization': 'Bearer ' + result['access_token']},).json()

    for v in graph_data["value"]:
        print(v["name"], ": ", v["id"])

else:
    print(result.get("error"))
    print(result.get("error_description"))
    print(result.get("correlation_id"))  
