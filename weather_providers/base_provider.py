import os
from abc import ABC, abstractmethod
import logging
import xml.etree.ElementTree as ET
from astral import LocationInfo
from astral.sun import sun
import datetime
import pytz
import requests


class BaseWeatherProvider(ABC):

    @abstractmethod
    def get_weather(self):
        """
        Implement this method.
        Return a dictionary in this format:
        { "temperatureMin": "2.0", "temperatureMax": "15.1", "icon": "mostly_cloudy", "description": "Cloudy with light breezes" }
        """
        pass

    def f_to_c(self, fahrenheit):
        """
        Return the Celsius value from a given Fahrenheit
        """
        return float((fahrenheit - 32) * 5/9)

    def c_to_f(self, celsius):
        """
        Return the Fahrenheit value from a given Celsius
        """
        return (float(celsius)*9/5) + 32

    def is_daytime(self, location_lat, location_long):
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

    def get_response_json(self, url, headers={}):
        """
        Perform an HTTP GET for a `url` with optional `headers`.
        Returns the response as JSON
        """
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_response_xml(self, url, headers={}):
        """
        Perform an HTTP GET for a `url` with optional `headers`.
        Returns the response as an XML ElementTree
        """
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return ET.fromstring(response.text)
