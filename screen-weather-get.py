#!/usr/bin/python

import json
import requests
from xml.dom import minidom
import datetime
import codecs
import os.path
import time
import sys
import os
import html


climacell_apikey=os.getenv("CLIMACELL_APIKEY","")

if climacell_apikey=="":
    print("CLIMACELL_APIKEY is missing")
    sys.exit(1)

town_lat='51.3656'
town_long='-0.1963'

template = 'screen-template.svg'


#Map Climacell icons to local icons
#Reference: https://developer.climacell.co/v3/reference#data-layers-core


icon_dict={
    'freezing_rain_heavy':'freezing_rain', 
    'freezing_rain':'freezing_rain', 
    'freezing_rain_light': 'freezing_rain' ,
    'freezing_drizzle': 'freezing_rain',
    'ice_pellets_heavy': 'ice_pellets',
    'ice_pellets': 'ice_pellets',
    'ice_pellets_light': 'rain_icepellets_mix',
    'snow_heavy': 'snow',
    'snow': 'snow',
    'snow_light': 'rain_snow_mix',
    'flurries': 'blizzard',
    'tstorm': 'thundershower_rain',
    'rain_heavy': 'rain_day',
    'rain': 'rain_day',
    'rain_light': 'rain_day',
    'drizzle': 'rain_day',
    'fog_light': 'scattered_clouds_fog',
    'fog': 'foggy',
    'cloudy': 'few_clouds',
    'mostly_cloudy':'mostly_cloudy',
    'partly_cloudy': 'few_clouds',
    'mostly_clear': 'clear_sky_day', 
    'clear': 'clear_sky_day'
}


weather_json=''
stale=True

if(os.path.isfile(os.getcwd() + "/apiresponse.json")):
    #Read the contents anyway
    with open(os.getcwd() + "/apiresponse.json", 'r') as content_file:
        weather_json = content_file.read()
    stale=time.time() - os.path.getmtime(os.getcwd() + "/apiresponse.json") > (1*60*60)

#If old file or file doesn't exist, time to download it
if(stale):
    try:
        print("Old file, attempting re-download")
        url = "https://api.climacell.co/v3/weather/forecast/daily?lat={}&lon={}&unit_system=si&start_time=now&fields=temp%2Cweather_code&apikey={}".format(town_lat, town_long, climacell_apikey)
        weather_json = requests.get(url).text
        with open(os.getcwd() + "/apiresponse.json", "w") as text_file:
            text_file.write(weather_json)
    except:
        print("Failed to get new API response, will use older response")
        with open(os.getcwd() + "/apiresponse.json", 'r') as content_file:
            weather_json = content_file.read()

weather_data = json.loads(weather_json)


#icon_one = weatherData['daily']['data'][0]['icon']
icon_one = weather_data[0]['weather_code']['value']
high_one = round(weather_data[0]['temp'][1]['max']['value'])
low_one = round(weather_data[0]['temp'][0]['min']['value'])
day_one = datetime.datetime.now().strftime('%a %b %d')
latest_alert=""

# if 'alerts' in weatherData:
#     latest_alert = html.escape(weatherData['alerts'][0]['title'])

print(icon_one , high_one, low_one, day_one)

# Process the SVG
output = codecs.open(template , 'r', encoding='utf-8').read()
output = output.replace('ICON_ONE',icon_dict[icon_one])
output = output.replace('HIGH_ONE',str(high_one))
output = output.replace('LOW_ONE',str(low_one)+"°C")
output = output.replace('DAY_ONE',day_one)

output = output.replace('TIME_NOW',datetime.datetime.now().strftime("%H:%M"))

output = output.replace('ALERT_MESSAGE', latest_alert)

codecs.open('screen-output-weather.svg', 'w', encoding='utf-8').write(output)





