import logging

from utility import get_response_data, is_daytime


# Map Accuweather icons to local icons
# Reference: https://developer.accuweather.com/weather-icons
def get_icon_from_accuweather_weathercode(weathercode, is_daytime):

    icon_dict = {
                    1: "clear_sky_day" if is_daytime else "clearnight",
                    2: "clear_sky_day" if is_daytime else "clearnight",
                    3: "few_clouds" if is_daytime else "partlycloudynight",
                    4: "scattered_clouds" if is_daytime else "partlycloudynight",
                    5: "haze",
                    6: "mostly_cloudy" if is_daytime else "overcast",
                    7: "climacell_cloudy" if is_daytime else 'overcast',
                    8: "overcast",
                    11: "climacell_fog",
                    12: 'climacell_rain_light' if is_daytime else 'rain_night',
                    13: 'climacell_rain_heavy' if is_daytime else 'rain_night',
                    14: 'climacell_rain_light' if is_daytime else 'rain_night',
                    15: "thundershower_rain",
                    16: "scattered_thundershowers",
                    17: "scattered_thundershowers",
                    18: "climacell_rain" if is_daytime else "rain_night",
                    19: "climacell_flurries",
                    20: "climacell_flurries",
                    21: "climacell_flurries",
                    22: "snow",
                    23: "snow",
                    24: "climacell_freezing_rain",
                    25: "climacell_freezing_rain",
                    26: "climacell_freezing_rain",
                    29: "sleet",
                    30: "very_hot",
                    31: "cold",
                    32: "wind",
                    33: "clear_sky_day" if is_daytime else "clearnight",
                    34: "clear_sky_day" if is_daytime else "clearnight",
                    35: "few_clouds" if is_daytime else "partlycloudynight",
                    36: "scattered_clouds" if is_daytime else "partlycloudynight",
                    37: "haze",
                    38: "mostly_cloudy" if is_daytime else "overcast",
                    39: 'climacell_rain_light' if is_daytime else 'rain_night',
                    40: 'climacell_rain_heavy' if is_daytime else 'rain_night',
                    41: "thundershower_rain",
                    42: "thundershower_rain",
                    43: "climacell_flurries",
                    44: "snow"
                }

    icon = icon_dict[weathercode]
    logging.debug(
         "get_icon_by_weathercode({}, {}) - {}"
         .format(weathercode, is_daytime, icon))

    return icon


# Get weather from Accuweather Daily Forecast API
# https://developer.accuweather.com/accuweather-forecast-api/apis/get/forecasts/v1/daily/1day/%7BlocationKey%7D
def get_weather(accuweather_apikey, location_lat, location_long, location_key, units):

    url = ("http://dataservice.accuweather.com/forecasts/v1/daily/1day/{}?apikey={}&details=true&metric={}"
           .format(location_key, accuweather_apikey, "true" if units == "metric" else "false"))
    try:
        response_data = get_response_data(url)
        weather_data = response_data
        logging.debug("get_weather() - {}".format(weather_data))
    except Exception as error:
        logging.error(error)
        weather = None

    daytime = is_daytime(location_lat, location_long)
    accuweather_icon = weather_data["DailyForecasts"][0]["Day"]["Icon"] if daytime else weather_data["DailyForecasts"][0]["Night"]["Icon"]
    # { "temperatureMin": "2.0", "temperatureMax": "15.1", "icon": "mostly_cloudy", "description": "Cloudy with light breezes" }
    weather = {}
    weather["temperatureMin"] = weather_data["DailyForecasts"][0]["Temperature"]["Minimum"]["Value"]
    weather["temperatureMax"] = weather_data["DailyForecasts"][0]["Temperature"]["Maximum"]["Value"]
    weather["icon"] = get_icon_from_accuweather_weathercode(accuweather_icon, daytime)
    weather["description"] = weather_data["DailyForecasts"][0]["Day"]["ShortPhrase"] if is_daytime(location_lat, location_long) else weather_data["DailyForecasts"][0]["Night"]["ShortPhrase"]
    logging.debug(weather)
    return weather
