import logging
import requests
import os
import json


from utility import get_response_data, is_stale, is_daytime
logging.basicConfig(level=logging.INFO)



# Map Climacell icons to local icons
# Reference: https://docs.climacell.co/reference/data-layers-core
def get_icon_from_climacell_weathercode(weathercode, is_daytime):


    icon_dict = {
           0: 'unknown',
        1000: 'clear_sky_day' if is_daytime else 'clearnight',
        1001: 'climacell_cloudy' if is_daytime else 'overcast',
        1100: 'few_clouds' if is_daytime else 'partlycloudynight',
        1101: 'scattered_clouds' if is_daytime else 'partlycloudynight',
        1102: 'mostly_cloudy' if is_daytime else 'overcast',
        2000: 'climacell_fog',
        2100: 'climacell_fog_light',
        3000: 'wind',
        3001: 'wind',
        3002: 'wind',
        4000: 'climacell_drizzle' if is_daytime else 'rain_night',
        4001: 'climacell_rain' if is_daytime else 'rain_night',
        4200: 'climacell_rain_light' if is_daytime else 'rain_night',
        4201: 'climacell_rain_heavy' if is_daytime else 'rain_night',
        5000: 'snow',
        5001: 'climacell_flurries',
        5100: 'climacell_snow_light',
        5101: 'snow',
        6000: 'climacell_freezing_drizzle',
        6001: 'climacell_freezing_rain',
        6200: 'climacell_freezing_rain_light' ,
        6201: 'climacell_freezing_rain_heavy',
        7000: 'climacell_ice_pellets',
        7101: 'climacell_ice_pellets_heavy',
        7102: 'climacell_ice_pellets_light',
        8000: 'thundershower_rain',
        }

    icon = icon_dict[weathercode]
    logging.debug(
         "get_icon_by_weathercode({}, {}) - {}"
         .format(weathercode, is_daytime, icon))

    return icon

def get_description_from_climacell_weathercode(weathercode):

    description_dict = {
        0: "Unknown",
        1000: "Clear",
        1001: "Cloudy",
        1100: "Mostly Clear",
        1101: "Partly Cloudy",
        1102: "Mostly Cloudy",
        2000: "Fog",
        2100: "Light Fog",
        3000: "Light Wind",
        3001: "Wind",
        3002: "Strong Wind",
        4000: "Drizzle",
        4001: "Rain",
        4200: "Light Rain",
        4201: "Heavy Rain",
        5000: "Snow",
        5001: "Flurries",
        5100: "Light Snow",
        5101: "Heavy Snow",
        6000: "Freezing Drizzle",
        6001: "Freezing Rain",
        6200: "Light Freezing Rain",
        6201: "Heavy Freezing Rain",
        7000: "Ice Pellets",
        7101: "Heavy Ice Pellets",
        7102: "Light Ice Pellets",
        8000: "Thunderstorm"
    }

    description=description_dict[weathercode]

    logging.debug(
         "get_description_by_weathercode({}) - {}"
         .format(weathercode, description))

    return description


# Get weather from Climacell
# Reference: https://docs.climacell.co/reference/retrieve-timelines-basic
def get_weather(climacell_apikey, location_lat, location_long, units):

    location_latlong = (
        "{0:.2f},{1:.2f}"
        .format(float(location_lat), float(location_long)))

    url = ("https://data.climacell.co/v4/timelines"
        + "?location={}&units={}&fields=temperatureMin&fields=temperatureMax&fields=weatherCode&timesteps=1d&apikey={}"
        .format(location_latlong, units, climacell_apikey))
    try:
        response_data = get_response_data(url)
        weather_data = response_data["data"]['timelines'][0]['intervals'][0]['values']
        logging.debug("get_weather() - {}".format(weather_data))
    except Exception as error:
        logging.error(error)
        weather = None

    # { "temperatureMin": "2.0", "temperatureMax": "15.1", "icon": "mostly_cloudy", "description": "Cloudy with light breezes" }
    weather = {}
    weather["temperatureMin"] = weather_data["temperatureMin"]
    weather["temperatureMax"] = weather_data["temperatureMax"]
    weather["icon"] = get_icon_from_climacell_weathercode(weather_data['weatherCode'], is_daytime(location_lat, location_long))
    weather["description"] = get_description_from_climacell_weathercode(weather_data['weatherCode'])
    logging.debug(weather)
    return weather