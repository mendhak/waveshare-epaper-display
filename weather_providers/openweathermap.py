import logging
from weather_providers.base_provider import BaseWeatherProvider


class OpenWeatherMap(BaseWeatherProvider):
    def __init__(self, openweathermap_apikey, location_lat, location_long, units):
        self.openweathermap_apikey = openweathermap_apikey
        self.location_lat = location_lat
        self.location_long = location_long
        self.units = units

    # Map OpenWeatherMap icons to local icons
    # Reference: https://openweathermap.org/weather-conditions
    def get_icon_from_openweathermap_weathercode(self, weathercode, is_daytime):

        icon_dict = {
                        200: "thundershower_rain",  # thunderstorm with light rain
                        201: "thundershower_rain",  # thunderstorm with rain
                        202: "thundershower_rain",  # thunderstorm with heavy rain
                        210: "thundershower_rain",  # light thunderstorm
                        211: "thundershower_rain",  # thunderstorm
                        212: "thundershower_rain",  # heavy thunderstorm
                        221: "thundershower_rain",  # ragged thunderstorm
                        230: "thundershower_rain",  # thunderstorm with light drizzle
                        231: "thundershower_rain",  # thunderstorm with drizzle
                        232: "thundershower_rain",  # thunderstorm with heavy drizzle
                        300: "climacell_drizzle" if is_daytime else "rain_night_light",  # light intensity drizzle
                        301: "climacell_drizzle" if is_daytime else "rain_night_light",  # drizzle
                        302: "climacell_rain" if is_daytime else "rain_night",  # heavy intensity drizzle
                        310: "climacell_drizzle" if is_daytime else "rain_night_light",  # light intensity drizzle rain
                        311: "climacell_drizzle" if is_daytime else "rain_night_light",  # drizzle rain
                        312: "climacell_rain" if is_daytime else "rain_night",  # heavy intensity drizzle rain
                        313: "climacell_rain" if is_daytime else "rain_night",  # shower rain and drizzle
                        314: "climacell_rain_heavy" if is_daytime else "rain_night_heavy",  # heavy shower rain and drizzle
                        321: "climacell_drizzle" if is_daytime else "rain_night_light",  # shower drizzle
                        500: "climacell_rain_light" if is_daytime else "rain_night_light",  # light rain
                        501: "climacell_rain" if is_daytime else "rain_night",  # moderate rain
                        502: "climacell_rain_heavy" if is_daytime else "rain_night_heavy",  # heavy intensity rain
                        503: "climacell_rain_heavy" if is_daytime else "rain_night_heavy",  # very heavy rain
                        504: "climacell_rain_heavy" if is_daytime else "rain_night_heavy",  # extreme rain
                        511: "climacell_freezing_rain",  # freezing rain
                        520: "climacell_rain_light" if is_daytime else "rain_night_light",  # light intensity shower rain
                        521: "climacell_rain" if is_daytime else "rain_night",  # shower rain
                        522: "climacell_rain_heavy" if is_daytime else "rain_night_heavy",  # heavy intensity shower rain
                        531: "climacell_rain" if is_daytime else "rain_night",  # ragged shower rain
                        600: "climacell_snow_light",  # light snow
                        601: "snow",  # Snow
                        602: "snow",  # Heavy snow
                        611: "sleet",  # Sleet
                        612: "sleet",  # Light shower sleet
                        613: "sleet",  # Shower sleet
                        615: "sleet",  # Light rain and snow
                        616: "sleet",  # Rain and snow
                        620: "climacell_snow_light",  # Light shower snow
                        621: "snow",  # Shower snow
                        622: "snow",  # Heavy shower snow
                        701: "climacell_fog",  # mist
                        711: "fire_smoke",  # Smoke
                        721: "climacell_fog",  # Haze
                        731: "dust_ash_sand",  # sand/ dust whirls
                        741: "climacell_fog",  # fog
                        751: "dust_ash_sand",  # sand
                        761: "dust_ash_sand",  # dust
                        762: "volcano",  # volcanic ash
                        771: "wind",    # squalls
                        781: "tornado_hurricane",    # tornado
                        800: "clear_sky_day" if is_daytime else "clearnight",  # clear sky
                        801: "few_clouds" if is_daytime else "partlycloudynight",  # few clouds: 11-25%
                        802: "scattered_clouds" if is_daytime else "partlycloudynight",  # scattered clouds: 25-50%
                        803: "mostly_cloudy" if is_daytime else "mostly_cloudy_night",  # broken clouds: 51-84%
                        804: "mostly_cloudy" if is_daytime else "mostly_cloudy_night",  # overcast clouds: 85-100%
                    }

        icon = icon_dict[weathercode]
        logging.debug(
            "get_icon_by_weathercode({}, {}) - {}"
            .format(weathercode, is_daytime, icon))

        return icon

    # Get weather from OpenWeatherMap One Call
    # https://openweathermap.org/api/one-call-api
    def get_weather(self):

        url = ("https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly&units={}&appid={}"
               .format(self.location_lat, self.location_long, self.units, self.openweathermap_apikey))
        response_data = self.get_response_json(url)
        logging.debug(response_data)
        weather_data = response_data["daily"][0]
        logging.debug("get_weather() - {}".format(weather_data))

        # { "temperatureMin": "2.0", "temperatureMax": "15.1", "icon": "mostly_cloudy", "description": "Cloudy with light breezes" }
        weather = {}
        weather["temperatureMin"] = weather_data["temp"]["min"]
        weather["temperatureMax"] = weather_data["temp"]["max"]
        weather["icon"] = self.get_icon_from_openweathermap_weathercode(weather_data["weather"][0]["id"], self.is_daytime(self.location_lat, self.location_long))
        weather["description"] = weather_data["weather"][0]["description"].title()
        logging.debug(weather)
        return weather
