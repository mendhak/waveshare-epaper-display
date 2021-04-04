import logging

from utility import get_response_data, is_daytime


# Map OpenWeatherMap icons to local icons
# Reference: https://openweathermap.org/weather-conditions
def get_icon_from_openweathermap_weathercode(weathercode, is_daytime):

    icon_dict = {
                    200: "thundershower_rain",
                    201: "thundershower_rain",
                    202: "thundershower_rain",
                    210: "thundershower_rain",
                    211: "thundershower_rain",
                    212: "thundershower_rain",
                    221: "thundershower_rain",
                    230: "thundershower_rain",
                    231: "thundershower_rain",
                    232: "thundershower_rain",
                    300: "climacell_drizzle" if is_daytime else "rain_night",
                    301: "climacell_drizzle" if is_daytime else "rain_night",
                    302: "climacell_rain" if is_daytime else "rain_night",
                    310: "climacell_drizzle" if is_daytime else "rain_night",
                    311: "climacell_drizzle" if is_daytime else "rain_night",
                    312: "climacell_rain" if is_daytime else "rain_night",
                    313: "climacell_rain" if is_daytime else "rain_night",
                    314: "climacell_rain_heavy" if is_daytime else "rain_night",
                    321: "climacell_drizzle" if is_daytime else "rain_night",
                    500: "climacell_rain_light" if is_daytime else "rain_night",
                    501: "climacell_rain" if is_daytime else "rain_night",
                    502: "climacell_rain_heavy" if is_daytime else "rain_night",
                    503: "climacell_rain_heavy" if is_daytime else "rain_night",
                    504: "climacell_rain_heavy" if is_daytime else "rain_night",
                    511: "climacell_freezing_rain",
                    520: "climacell_rain_light" if is_daytime else "rain_night",
                    521: "climacell_rain" if is_daytime else "rain_night",
                    522: "climacell_rain_heavy" if is_daytime else "rain_night",
                    531: "climacell_rain" if is_daytime else "rain_night",
                    600: "climacell_snow_light",
                    601: "snow",
                    602: "snow",
                    611: "rain_snow_mix",
                    612: "rain_snow_mix",
                    613: "rain_snow_mix",
                    615: "rain_snow_mix",
                    616: "rain_snow_mix",
                    620: "climacell_snow_light",
                    621: "snow",
                    622: "snow",
                    701: "climacell_fog",
                    711: "fire_smoke",
                    721: "climacell_fog",
                    731: "dust_ash_sand",  # sand/dust whirls
                    741: "climacell_fog",
                    751: "dust_ash_sand",  # sand
                    761: "dust_ash_sand",  # dust
                    762: "dust_ash_sand",  # ash
                    771: "wind",  # squall
                    781: "volcano",  # volcanic ash
                    800: "clear_sky_day" if is_daytime else "clearnight",
                    801: "few_clouds" if is_daytime else "partlycloudynight",
                    802: "scattered_clouds" if is_daytime else "partlycloudynight",
                    803: "mostly_cloudy" if is_daytime else "overcast",
                    804: "mostly_cloudy" if is_daytime else "overcast",
                }

    icon = icon_dict[weathercode]
    logging.debug(
         "get_icon_by_weathercode({}, {}) - {}"
         .format(weathercode, is_daytime, icon))

    return icon


# Get weather from OpenWeatherMap One Call
# https://openweathermap.org/api/one-call-api
def get_weather(openweathermap_apikey, location_lat, location_long, units):

    url = ("https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly&units={}&appid={}"
           .format(location_lat, location_long, units, openweathermap_apikey))
    try:
        response_data = get_response_data(url)
        logging.debug(response_data)
        weather_data = response_data["daily"][0]
        logging.debug("get_weather() - {}".format(weather_data))
    except Exception as error:
        logging.error(error)
        weather = None

    # { "temperatureMin": "2.0", "temperatureMax": "15.1", "icon": "mostly_cloudy", "description": "Cloudy with light breezes" }
    weather = {}
    weather["temperatureMin"] = weather_data["temp"]["min"]
    weather["temperatureMax"] = weather_data["temp"]["max"]
    weather["icon"] = get_icon_from_openweathermap_weathercode(weather_data["weather"][0]["id"], is_daytime(location_lat, location_long))
    weather["description"] = weather_data["weather"][0]["description"].title()
    logging.debug(weather)
    return weather
