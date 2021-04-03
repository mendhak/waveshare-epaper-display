#!/usr/bin/python

import datetime
import sys
import os
import logging
from weather_providers import climacell
from utility import is_stale, update_svg

logging.basicConfig(level=logging.INFO)

def main():

    # gather relevant environment configs
    climacell_apikey=os.getenv("CLIMACELL_APIKEY")
    if not climacell_apikey:
        logging.error("CLIMACELL_APIKEY is missing")
        sys.exit(1)

    weather_format=os.getenv("WEATHER_FORMAT", "CELSIUS")
    if (weather_format == "CELSIUS"):
        units = "metric"
    else:
        units = "imperial"

    location_lat = os.getenv("WEATHER_LATITUDE","51.3656") 
    location_long = os.getenv("WEATHER_LONGITUDE","-0.1963") 

    # TTL for refetching of JSON
    ttl = float(os.getenv("WEATHER_TTL", 1 * 60 * 60))

    if climacell_apikey:
        logging.info("Gathering weather from Climacell")
        weather_timelines_filename = 'climacell-timelines-response.json'
        weather = climacell.get_weather(climacell_apikey, location_lat, location_long, units, weather_timelines_filename, ttl)

    if not weather:
        logging.error("Unable to fetch weather payload. SVG will not be updated.")
        return

    degrees = "°C" if units == "metric" else "°F"

    output_dict = {
        'LOW_ONE': "{}{}".format(str(round(weather['temperatureMin'])), degrees),
        'HIGH_ONE': "{}{}".format(str(round(weather['temperatureMax'])), degrees),
        'ICON_ONE': weather["icon"],
        'WEATHER_DESC': weather["description"],
        'TIME_NOW': datetime.datetime.now().strftime("%-I:%M %p"),
        'DAY_ONE': datetime.datetime.now().strftime("%b %-d, %Y"),
        'DAY_NAME': datetime.datetime.now().strftime("%A"),
        'ALERT_MESSAGE': "" # unused
    }

    logging.debug("main() - {}".format(output_dict))

    logging.info("Updating SVG")
    template_svg_filename = 'screen-template.svg'
    output_svg_filename = 'screen-output-weather.svg'
    update_svg(template_svg_filename, output_svg_filename, output_dict)


if __name__ == "__main__":
    main()
