#!/usr/bin/python

# Kindle Weather Display
# Matthew Petroff (http://www.mpetroff.net/)
# September 2012
#
# Owen Bullock - UK Weather - MetOffice - Aug 2013
# Apr 2014 - amended for Wind option
# Mendhak Apr 2017 - redone for WeatherUnderground API
# Mendhak Apr 2019 - redone for OpenWeatherMap

import json
import requests
from xml.dom import minidom
import datetime
import codecs
import os.path
import time
import sys
import os


template = 'screen-template.svg'

#Map OpenWeatherMap icons to local icons
#Reference: https://openweathermap.org/weather-conditions

icon_dict={
    '01d':'skc',
    '01n':'skc',
    '02d':'sct',
    '02n':'sct',
    '03d':'sct',
    '03n':'sct',
    '04d':'bkn',
    '04n':'bkn',
    '09d':'ra',
    '09n':'ra',
    '10d':'ra',
    '11d':'tsra',
    '11n':'tsra',
    '13d':'sn',
    '13n':'sn',
    '50d':'fg',
    '50n':'fg'
}



#
# Download and parse weather data - location 2636503 = Sutton, Surrey
#

weather_json=''
stale=True

if(os.path.isfile(os.getcwd() + "/apiresponse.json")):
    #Read the contents anyway
    with open(os.getcwd() + "/apiresponse.json", 'r') as content_file:
        weather_json = content_file.read()
    stale=time.time() - os.path.getmtime(os.getcwd() + "/apiresponse.json") > (12*60*60)

#If old file or file doesn't exist, time to download it
if(stale):
    try:
        print("Old file, attempting re-download")
        url='https://samples.openweathermap.org/data/2.5/forecast?id=524901&appid=b6907d289e10d714a6e88b30761fae22'
        weather_json = requests.get(url).text
        with open(os.getcwd() + "/apiresponse.json", "w") as text_file:
            text_file.write(json.dumps(weather_json))
    except:
        print("Failed to get new API response, will use older response")
        with open(os.getcwd() + "/apiresponse.json", 'r') as content_file:
            weather_json = content_file.read()

weatherData = json.loads(weather_json)

icon_one = weatherData['list'][0]['weather'][0]['icon']
high_one = round(weatherData['list'][0]['main']['temp_max'] - 273.15, 2)
low_one = round(weatherData['list'][0]['main']['temp_min'] - 273.15, 2)
day_one = time.strftime('%A', time.localtime(weatherData['list'][0]['dt']))

print(icon_one , high_one, low_one, day_one)

# Process the SVG
output = codecs.open(template , 'r', encoding='utf-8').read()
output = output.replace('ICON_ONE',icon_dict[icon_one])
output = output.replace('HIGH_ONE',str(high_one))
output = output.replace('LOW_ONE',str(low_one)+"°C")
output = output.replace('DAY_ONE',day_one)

output = output.replace('ICON_TWO',"")
output = output.replace('HIGH_TWO',"")
output = output.replace('LOW_TWO',"")

output = output.replace('ICON_THREE',"")
output = output.replace('HIGH_THREE',"")
output = output.replace('LOW_THREE',"")

output = output.replace('TIME_NOW',datetime.datetime.now().strftime("%H:%M"))

dtnow=datetime.datetime.now().strftime("%d-%b %H:%M")
output = output.replace('DATE_VALPLACE',str(dtnow))
readableDate = datetime.datetime.now().strftime("%A %B %d")
output = output.replace('TODAY_DATE', str(readableDate))

codecs.open('screen-output-weather.svg', 'w', encoding='utf-8').write(output)





