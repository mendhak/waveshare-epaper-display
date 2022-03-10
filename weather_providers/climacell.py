import logging
from weather_providers.base_provider import BaseWeatherProvider


class Climacell(BaseWeatherProvider):
    def __init__(self, climacell_apikey, location_lat, location_long, units):
        self.climacell_apikey = climacell_apikey
        self.location_lat = location_lat
        self.location_long = location_long
        self.units = units

    # Map Climacell icons to local icons
    # Reference: https://docs.tomorrow.io/reference/data-layers-core#data-layers-weather-codes
    def get_icon_from_climacell_weathercode(self, weathercode, is_daytime):

        icon_dict = {
                        0: 'unknown',
                        1000: 'clear_sky_day' if is_daytime else 'clearnight',  # Clear, Sunny
                        1001: 'climacell_cloudy' if is_daytime else 'overcast',  # Cloudy
                        1100: 'few_clouds' if is_daytime else 'partlycloudynight',  # Mostly Clear
                        1101: 'scattered_clouds' if is_daytime else 'partlycloudynight',  # Partly Cloudy
                        1102: 'mostly_cloudy' if is_daytime else 'mostly_cloudy_night',  # Mostly Cloudy
                        2000: 'climacell_fog',  # Fog
                        2100: 'climacell_fog_light',  # Light Fog
                        3000: 'wind',  # Removed?
                        3001: 'wind',  # Removed?
                        3002: 'wind',  # Removed?
                        4000: 'climacell_drizzle' if is_daytime else 'rain_night_light',  # Drizzle
                        4001: 'climacell_rain' if is_daytime else 'rain_night',  # Rain
                        4200: 'climacell_rain_light' if is_daytime else 'rain_night_light',  # Light Rain
                        4201: 'climacell_rain_heavy' if is_daytime else 'rain_night_heavy',  # Heavy Rain
                        5000: 'snow',  # Snow
                        5001: 'climacell_flurries',  # Flurries
                        5100: 'climacell_snow_light',  # Light Snow
                        5101: 'snow',  # Heavy Snow
                        6000: 'climacell_freezing_drizzle',  # Freezing Drizzle
                        6001: 'climacell_freezing_rain',  # Freezing Rain
                        6200: 'climacell_freezing_rain_light',  # Light Freezing Rain
                        6201: 'climacell_freezing_rain_heavy',  # Heavy Freezing Rain
                        7000: 'climacell_ice_pellets',  # Ice Pellets
                        7101: 'climacell_ice_pellets_heavy',  # Heavy Ice Pellets
                        7102: 'climacell_ice_pellets_light',  # Light Ice Pellets
                        8000: 'thundershower_rain'  # Thunderstorm
                    }

        icon = icon_dict[weathercode]
        logging.debug(
            "get_icon_by_weathercode({}, {}) - {}"
            .format(weathercode, is_daytime, icon))

        return icon

    def get_description_from_climacell_weathercode(self, weathercode):

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

        description = description_dict[weathercode]

        logging.debug(
            "get_description_by_weathercode({}) - {}"
            .format(weathercode, description))

        return description

    # Get weather from Climacell
    # Reference: https://docs.climacell.co/reference/retrieve-timelines-basic
    def get_weather(self):

        location_latlong = (
            "{0:.2f},{1:.2f}"
            .format(float(self.location_lat), float(self.location_long)))

        url = ("https://data.climacell.co/v4/timelines"
               + "?location={}&units={}&fields=temperatureMin&fields=temperatureMax&fields=weatherCode&timesteps=1d&apikey={}"
               .format(location_latlong, self.units, self.climacell_apikey))

        response_data = self.get_response_json(url)
        weather_data = response_data["data"]['timelines'][0]['intervals'][0]['values']
        logging.debug("get_weather() - {}".format(weather_data))

        daytime = self.is_daytime(self.location_lat, self.location_long)
        # { "temperatureMin": "2.0", "temperatureMax": "15.1", "icon": "mostly_cloudy", "description": "Cloudy with light breezes" }
        weather = {}
        weather["temperatureMin"] = weather_data["temperatureMin"]
        weather["temperatureMax"] = weather_data["temperatureMax"]
        weather["icon"] = self.get_icon_from_climacell_weathercode(weather_data['weatherCode'], daytime)
        weather["description"] = self.get_description_from_climacell_weathercode(weather_data['weatherCode'])
        logging.debug(weather)
        return weather
