#!/usr/bin/python

import json
import requests
import datetime
import codecs
import os.path
import time
import sys
import os
import html
import pytz
import logging
from astral import LocationInfo
from astral.sun import sun

logging.basicConfig(level=logging.INFO)

# Map Climacell icons to local icons
# Reference: https://docs.climacell.co/reference/data-layers-core
def get_icon_by_weathercode(weathercode, is_daytime):

    icon_dict = {
        6201: 'freezing_rain',
    	6001: 'freezing_rain',
    	6200: 'freezing_rain' ,
    	6000: 'freezing_rain',
    	7101: 'ice_pellets',
    	7000: 'ice_pellets',
	7102: 'rain_icepellets_mix',
    	5101: 'snow',
    	5000: 'snow',
    	5100: 'rain_snow_mix',
    	5001: 'blizzard',
    	8000: 'thundershower_rain',
    	4201: 'rain_day' if is_daytime else 'rain_night',
    	4001: 'rain_day' if is_daytime else 'rain_night',
    	4200: 'rain_day' if is_daytime else 'rain_night',
    	4000: 'rain_day' if is_daytime else 'rain_night',
    	2100: 'scattered_clouds_fog',
    	2000: 'foggy',
    	1001: 'few_clouds' if is_daytime else 'partlycloudynight',
    	1102: 'mostly_cloudy',
    	1101: 'few_clouds' if is_daytime else 'partlycloudynight',
    	1100: 'clear_sky_day' if is_daytime else 'clearnight',
    	1000: 'clear_sky_day' if is_daytime else 'clearnight',
    	3000: 'wind',
    	3001: 'wind',
    	3002: 'wind',
	}

    icon = icon_dict[weathercode]
    logging.debug(
         "get_icon_by_weathercode({}, {}) - {}"
         .format(weathercode, is_daytime, icon))

    return icon

# Is it daytime? 
def is_daytime(location_lat, location_long):

    # adjust icon for sunrise and sunset
    dt = datetime.datetime.now(pytz.utc)
    city = LocationInfo(location_lat, location_long)
    s = sun(city.observer, date=dt)
    verdict = False
    if dt > s['sunset'] or dt < s['sunrise']:
        verdict = False
    else:
        verdict = True

    logging.debug(
        "is_daytime({}{}) - {}"
        .format(str(location_lat), str(location_long), str(verdict)))

    return verdict


# Get weather from Climacell
# Reference: https://docs.climacell.co/reference/retrieve-timelines-basic
def get_weather(climacell_apikey, location_latlong, filename, ttl):

    url = ("https://data.climacell.co/v4/timelines"
        + "?location={}&fields=temperatureMin&fields=temperatureMax&fields=weatherCode&timesteps=1d&apikey={}"
        .format(location_latlong, climacell_apikey))

    try:
        response_data = get_response_data(url, os.getcwd() + "/" + filename, ttl)
        weather = response_data['timelines'][0]['intervals'][0]['values']
        logging.debug("get_weather() - {}".format(weather))
    except Exception as error:
        logging.error(error)
        weather = False

    return weather

def get_response_data(url, filepath, ttl):

    response_json = False

    if (is_stale(filepath, ttl)):
        try:
            response_data = requests.get(url).text
            response_json = json.loads(response_data)['data']
            with open(filepath, 'w') as text_file:
                text_file.write(response_data)
        except Exception as error:
            logging.error(error)
            raise
    else:
        with open(filepath, 'r') as file:
            return json.loads(file.read())['data']
    return response_json

# Is the response file older than the TTL?
def is_stale(filepath, ttl): 

    verdict = True
    if (os.path.isfile(filepath)):
        verdict = time.time() - os.path.getmtime(filepath) > ttl

    logging.debug(
        "is_stale({}) - {}"
        .format(filepath, str(verdict)))

    return verdict

# utilize a template svg as a base for output of values
def update_svg(template_svg_filename, output_svg_filename, output_dict):
    #replace tags with values in SVG
    output = codecs.open(template_svg_filename, 'r', encoding='utf-8').read()

    for output_key in output_dict:
        logging.debug("output_weather() - {} -> {}".format(output_key, output_dict[output_key]))
        output = output.replace(output_key, output_dict[output_key])

    logging.debug("update_svg() - Write to SVG {}".format(output_svg_filename))

    codecs.open(output_svg_filename, 'w', encoding='utf-8').write(output)


def main():

    # gather relevant environment configs

    climacell_apikey=os.getenv("CLIMACELL_APIKEY","")

    if climacell_apikey=="":
        logging.error("CLIMACELL_APIKEY is missing")
        sys.exit(1)

    weather_format=os.getenv("WEATHER_FORMAT", "CELSIUS")

    template_svg_filename = 'screen-template.svg'
    output_svg_filename = 'screen-output-weather.svg'

    # json response files
    weather_timelines_filename = 'climacell-timelines-response.json'

    location_lat = os.getenv("WEATHER_LATITUDE","51.3656") 
    location_long = os.getenv("WEATHER_LONGITUDE","-0.1963") 

    location_latlong = (
        "{0:.2f},{1:.2f}"
        .format(float(location_lat), float(location_long)))

    # TTL for refetching of JSON
    ttl = float(os.getenv("WEATHER_TTL", 1 * 60 * 60))

    logging.info("Gathering weather") 

    weather = get_weather(climacell_apikey, location_latlong, weather_timelines_filename, ttl)

    if (weather == False):
        logging.error("Unable to fetch weather payload. SVG will not be updated.")
        return

    output_dict = {
        'LOW_ONE': str(round(weather['temperatureMin']))+"°C" if weather_format == "CELSIUS" else str(round(weather['temperatureMin'] * 1.8) + 32)+"°F", 
        'HIGH_ONE': str(round(weather['temperatureMax']))+"°C" if weather_format == "CELSIUS" else str(round(weather['temperatureMax'] * 1.8) + 32)+"°F", 
        'ICON_ONE': get_icon_by_weathercode(weather['weatherCode'], is_daytime(location_lat, location_long)),
        'TIME_NOW': datetime.datetime.now().strftime("%-I:%M %p"),
        'DAY_ONE': datetime.datetime.now().strftime("%d %b %Y"),
        'DAY_NAME': datetime.datetime.now().strftime("%A"),
        'ALERT_MESSAGE': "" # unused
    }

    logging.debug("main() - {}".format(output_dict))

    logging.info("Updating SVG")
    update_svg(template_svg_filename, output_svg_filename, output_dict)


if __name__ == "__main__":
    main()
