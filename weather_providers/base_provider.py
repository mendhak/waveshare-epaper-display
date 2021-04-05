import os
from abc import ABC, abstractmethod
from utility import is_stale
import logging
import json
import requests
from astral import LocationInfo
from astral.sun import sun
import datetime
import pytz


class BaseWeatherProvider(ABC):

    ttl = float(os.getenv("WEATHER_TTL", 1 * 60 * 60))
    cache_weather_file = "weather-cache.json"

    @abstractmethod
    def get_weather(self):
        """
        Implement this method.
        Return a dictionary in this format:
        { "temperatureMin": "2.0", "temperatureMax": "15.1", "icon": "mostly_cloudy", "description": "Cloudy with light breezes" }
        """
        pass

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

    def get_response_data(self, url, headers={}):
        """
        Perform an HTTP GET for a `url` with optional `headers`.
        Caches the response in weather-cache.json for WEATHER_TTL seconds.
        Returns the response as JSON
        """
        response_json = False

        if (is_stale(self.cache_weather_file, self.ttl)):
            logging.info("Cache file is stale. Fetching from source.")
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                response_data = response.text
                response_json = json.loads(response_data)
                with open(self.cache_weather_file, 'w') as text_file:
                    json.dump(response_json, text_file, indent=4)
            except Exception as error:
                logging.error(error)
                logging.error(response.text)
                logging.error(response.headers)
                raise
        else:
            logging.info("Found in cache.")
            with open(self.cache_weather_file, 'r') as file:
                return json.loads(file.read())
        return response_json
