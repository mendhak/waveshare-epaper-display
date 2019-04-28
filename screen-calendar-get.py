from __future__ import print_function
import datetime
import time
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import codecs

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
template = 'screen-output-weather.svg'


creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server()
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('calendar', 'v3', credentials=creds)


events_result = None
stale = True

if(os.path.isfile(os.getcwd() + "/calendar.pickle")):
    print("Found cached calendar response")
    with open('calendar.pickle','rb') as cal:
        events_result = pickle.load(cal)
    stale=time.time() - os.path.getmtime(os.getcwd() + "/calendar.pickle") > (1*60*60)

if stale:
    print("Pickle is stale, calling the Calendar API")
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    with open('calendar.pickle', 'wb') as cal:
        pickle.dump(events_result, cal)

events = events_result.get('items', [])

if not events:
    print('No upcoming events found.')

event_one = events[0]
start = event_one['start'].get('dateTime', event_one['start'].get('date'))
start = start[:10]
day_one = time.strftime("%a %b %d",time.strptime(start,"%Y-%m-%d"))
desc_one = event_one['summary']
print(day_one, desc_one)

event_two = events[1]
start = event_two['start'].get('dateTime', event_two['start'].get('date'))
start = start[:10]
day_two = time.strftime("%a %b %d",time.strptime(start,"%Y-%m-%d"))
desc_two = event_two['summary']
print(day_two, desc_two)



output = codecs.open(template , 'r', encoding='utf-8').read()
output = output.replace('CAL_ONE',day_one)
output = output.replace('CAL_DESC_ONE',desc_one)
output = output.replace('CAL_TWO',day_two)
output = output.replace('CAL_DESC_TWO',desc_two)

codecs.open('screen-output-weather.svg', 'w', encoding='utf-8').write(output)
