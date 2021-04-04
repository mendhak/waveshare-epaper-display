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


def configure_logging():
    """
    Sets up logging with a specific logging format.
    Call this at the beginning of a script.
    Then using logging methods as normal
    """
    log_level = os.getenv("LOG_LEVEL", "INFO")
    log_format = "%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s"
    log_dateformat = "%Y-%m-%d:%H:%M:%S"
    logging.basicConfig(level=log_level, format=log_format, datefmt=log_dateformat)
    logger = logging.getLogger()
    logger.setLevel(level=log_level)
    formatter = logging.Formatter(fmt=log_format, datefmt=log_dateformat)
    handler = logger.handlers[0]
    handler.setFormatter(formatter)


# utilize a template svg as a base for output of values
def update_svg(template_svg_filename, output_svg_filename, output_dict):
    """
    Update the `template_svg_filename` SVG.
    Replaces keys with values from `output_dict`
    Writes the output to `output_svg_filename`
    """
    # replace tags with values in SVG
    output = codecs.open(template_svg_filename, 'r', encoding='utf-8').read()

    for output_key in output_dict:
        logging.debug("update_svg() - {} -> {}"
                      .format(output_key, output_dict[output_key]))
        output = output.replace(output_key, output_dict[output_key])

    logging.debug("update_svg() - Write to SVG {}".format(output_svg_filename))

    codecs.open(output_svg_filename, 'w', encoding='utf-8').write(output)


def is_stale(filepath, ttl):
    """
    Checks if the specified `filepath` is older than the `ttl` in seconds
    Returns true if the file doesn't exist.
    """

    verdict = True
    if (os.path.isfile(filepath)):
        verdict = time.time() - os.path.getmtime(filepath) > ttl

    logging.debug(
        "is_stale({}) - {}"
        .format(filepath, str(verdict)))

    return verdict


def get_response_data(url, headers={}):
    """
    Perform an HTTP GET for a `url` with optional `headers`.
    Returns the response as JSON
    """

    response_json = False

    try:
        response_data = requests.get(url, headers=headers).text
        response_json = json.loads(response_data)
    except Exception as error:
        logging.error(error)
        raise

    return response_json


def is_daytime(location_lat, location_long):
    """
    Return whether it's daytime for a given lat/long.
    """

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
        "is_daytime({}, {}) - {}"
        .format(str(location_lat), str(location_long), str(verdict)))

    return verdict


def c_to_f(celsius):
    """
    Return the Fahrenheit value from a given Celsius
    """
    return (float(celsius)*9/5) + 32
