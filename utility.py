import codecs
import logging
import os
import time
import requests
import json
from astral import LocationInfo
from astral.sun import sun
import datetime
import pytz

logging.basicConfig(level=logging.INFO)

# utilize a template svg as a base for output of values
def update_svg(template_svg_filename, output_svg_filename, output_dict):

    #replace tags with values in SVG
    output = codecs.open(template_svg_filename, 'r', encoding='utf-8').read()

    for output_key in output_dict:
        logging.debug("update_svg() - {} -> {}".format(output_key, output_dict[output_key]))
        output = output.replace(output_key, output_dict[output_key])

    logging.debug("update_svg() - Write to SVG {}".format(output_svg_filename))

    codecs.open(output_svg_filename, 'w', encoding='utf-8').write(output)


# Is the response file older than the TTL?
def is_stale(filepath, ttl): 

    verdict = True
    if (os.path.isfile(filepath)):
        verdict = time.time() - os.path.getmtime(filepath) > ttl

    logging.debug(
        "is_stale({}) - {}"
        .format(filepath, str(verdict)))

    return verdict


# Make HTTP Request or get response from cached file
def get_response_data(url, filepath, ttl):

    response_json = False

    if (is_stale(filepath, ttl)):
        try:
            response_data = requests.get(url).text
            response_json = json.loads(response_data)
            with open(filepath, 'w') as text_file:
                text_file.write(response_data)
        except Exception as error:
            logging.error(error)
            raise
    else:
        with open(filepath, 'r') as file:
            return json.loads(file.read())
    return response_json


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