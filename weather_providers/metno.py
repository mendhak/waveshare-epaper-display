import logging
from weather_providers.base_provider import BaseWeatherProvider


class MetNo(BaseWeatherProvider):
    def __init__(self, metno_self_id, location_lat, location_long, units):
        self.metno_self_id = metno_self_id
        self.location_lat = location_lat
        self.location_long = location_long
        self.units = units

    # Map Met.no icons to local icons
    # Reference: https://api.met.no/weatherapi/weathericon/2.0/documentation
    def get_icon_from_metno_weathercode(self, weathercode, is_daytime):

        icon_dict = {
                        "clearsky": "clear_sky_day" if is_daytime else "clearnight",
                        "cloudy": "mostly_cloudy" if is_daytime else "mostly_cloudy_night",
                        "fair": "scattered_clouds" if is_daytime else "partlycloudynight",
                        "fog": "climacell_fog",
                        "heavyrain": "climacell_rain_heavy" if is_daytime else "rain_night_heavy",
                        "heavyrainandthunder": "thundershower_rain",
                        "heavyrainshowers": "climacell_rain_heavy" if is_daytime else "rain_night_heavy",
                        "heavyrainshowersandthunder": "thundershower_rain",
                        "heavysleet": "sleet",
                        "heavysleetandthunder": "sleet",
                        "heavysleetshowers": "sleet",
                        "heavysleetshowersandthunder": "sleet",
                        "heavysnow": "snow",
                        "heavysnowandthunder": "snow",
                        "heavysnowshowers": "snow",
                        "heavysnowshowersandthunder": "snow",
                        "lightrain": "climacell_rain_light" if is_daytime else "rain_night_light",
                        "lightrainandthunder": "climacell_rain_light" if is_daytime else "rain_night_light",
                        "lightrainshowers": "climacell_rain_light" if is_daytime else "rain_night_light",
                        "lightrainshowersandthunder": "climacell_rain_light" if is_daytime else "rain_night_light",
                        "lightsleet": "sleet",
                        "lightsleetandthunder": "sleet",
                        "lightsleetshowers": "sleet",
                        "lightsnow": "climacell_snow_light",
                        "lightsnowandthunder": "climacell_snow_light",
                        "lightsnowshowers": "climacell_snow_light",
                        "lightssleetshowersandthunder": "climacell_snow_light",
                        "lightssnowshowersandthunder": "climacell_snow_light",
                        "partlycloudy": "few_clouds" if is_daytime else "partlycloudynight",
                        "rain": "climacell_rain" if is_daytime else "rain_night",
                        "rainandthunder": "thundershower_rain",
                        "rainshowers": "climacell_rain" if is_daytime else "rain_night",
                        "rainshowersandthunder": "thundershower_rain",
                        "sleet": "sleet",
                        "sleetandthunder": "thundershower_rain",
                        "sleetshowers": "sleet",
                        "sleetshowersandthunder": "thundershower_rain",
                        "snow": "snow",
                        "snowandthunder": "snow",
                        "snowshowers": "snow",
                        "snowshowersandthunder": "snow"
                    }

        icon = icon_dict[weathercode]
        logging.debug(
            "get_icon_by_weathercode({}, {}) - {}"
            .format(weathercode, is_daytime, icon))

        return icon

    def get_description_from_metno_weathercode(self, weathercode):
        description_dict = {
                            "clearsky":	"Clear sky",
                            "cloudy":	"Cloudy",
                            "fair":	"Fair",
                            "fog":	"Fog",
                            "heavyrain":	"Heavy rain",
                            "heavyrainandthunder":	"Heavy rain and thunder",
                            "heavyrainshowers":	"Heavy rain showers",
                            "heavyrainshowersandthunder":	"Heavy rain showers and thunder",
                            "heavysleet":	"Heavy sleet",
                            "heavysleetandthunder":	"Heavy sleet and thunder",
                            "heavysleetshowers":	"Heavy sleet showers",
                            "heavysleetshowersandthunder":	"Heavy sleet showers and thunder",
                            "heavysnow":	"Heavy snow",
                            "heavysnowandthunder":	"Heavy snow and thunder",
                            "heavysnowshowers":	"Heavy snow showers",
                            "heavysnowshowersandthunder":	"Heavy snow showers and thunder",
                            "lightrain":	"Light rain",
                            "lightrainandthunder":	"Light rain and thunder",
                            "lightrainshowers":	"Light rain showers",
                            "lightrainshowersandthunder":	"Light rain showers and thunder",
                            "lightsleet":	"Light sleet",
                            "lightsleetandthunder":	"Light sleet and thunder",
                            "lightsleetshowers":	"Light sleet showers",
                            "lightsnow":	"Light snow",
                            "lightsnowandthunder":	"Light snow and thunder",
                            "lightsnowshowers":	"Light snow showers",
                            "lightssleetshowersandthunder":	"Light sleet showers and thunder",
                            "lightssnowshowersandthunder":	"Light snow showers and thunder",
                            "partlycloudy":	"Partly cloudy",
                            "rain":	"Rain",
                            "rainandthunder":	"Rain and thunder",
                            "rainshowers":	"Rain showers",
                            "rainshowersandthunder":	"Rain showers and thunder",
                            "sleet":	"Sleet",
                            "sleetandthunder":	"Sleet and thunder",
                            "sleetshowers":	"Sleet showers",
                            "sleetshowersandthunder":	"Sleet showers and thunder",
                            "snow":	"Snow",
                            "snowandthunder":	"Snow and thunder",
                            "snowshowers":	"Snow showers",
                            "snowshowersandthunder":	"Snow showers and thunder",
                        }

        description = description_dict[weathercode]

        logging.debug(
            "get_description_by_weathercode({}) - {}"
            .format(weathercode, description))

        return description

    # Get weather from Met.no API
    # https://api.met.no/weatherapi/locationforecast/2.0/documentation#!/data/get_complete
    # Met.no API only provides min/max temperatures and codes in 6 hour slots.
    # It would take more complex logic to walk through the forecast and get the weather code, min and max for the day.
    def get_weather(self):

        url = ("https://api.met.no/weatherapi/locationforecast/2.0/complete.json?lat={}&lon={}"
               .format(self.location_lat, self.location_long))

        headers = {"User-Agent": self.metno_self_id}

        response_data = self.get_response_json(url, headers=headers)
        logging.debug(response_data)
        weather_data = response_data["properties"]["timeseries"][0]["data"]
        logging.debug("get_weather() - {}".format(weather_data))

        # Remove the _night or _day suffix from Met.no symbol code, so we can do some mapping.
        weather_code = weather_data["next_6_hours"]["summary"]["symbol_code"].replace("_day", "").replace("_night", "")
        daytime = self.is_daytime(self.location_lat, self.location_long)

        # { "temperatureMin": "2.0", "temperatureMax": "15.1", "icon": "mostly_cloudy", "description": "Cloudy with light breezes" }
        weather = {}
        weather["temperatureMin"] = weather_data["next_6_hours"]["details"]["air_temperature_min"]
        weather["temperatureMax"] = weather_data["next_6_hours"]["details"]["air_temperature_max"]
        weather["icon"] = self.get_icon_from_metno_weathercode(weather_code, daytime)
        weather["description"] = self.get_description_from_metno_weathercode(weather_code)
        logging.debug(weather)
        return weather
