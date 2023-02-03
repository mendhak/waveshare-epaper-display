import logging
from weather_providers.base_provider import BaseWeatherProvider


class SMHI(BaseWeatherProvider):
    def __init__(self, smhi_self_id, location_lat, location_long, units):
        self.smhi_self_id = smhi_self_id
        self.location_lat = location_lat
        self.location_long = location_long
        self.units = units

    # Map SMHI icons to local icons
    # Reference: https://opendata.smhi.se/apidocs/metfcst/parameters.html#parameter-wsymb
    def get_icon_from_smhi_weathercode(self, weathercode, is_daytime):


        icon_dict = {
                        1: "clear_sky_day" if is_daytime else "clearnight", # Clear sky
                        2: "clear_sky_day" if is_daytime else "clearnight",  # Nearly clear sky
                        3: "few_clouds" if is_daytime else "partlycloudynight", # Variable cloudiness
                        4: "scattered_clouds" if is_daytime else "partlycloudynight", # Halfclear sky
                        5: "mostly_cloudy" if is_daytime else "mostly_cloudy_night", # Cloudy sky
                        6: "overcast", # Overcast
                        7: "climacell_fog", # Fog
                        8: 'climacell_rain_light' if is_daytime else 'rain_night_light', # Light rain showers
                        9: "climacell_rain" if is_daytime else "rain_night", # Moderate rain showers
                        10: "climacell_rain_heavy" if is_daytime else "rain_night_heavy", # Heavy rain showers
                        11: "thundershower_rain", # Thunderstorm
                        12: "sleet", # Light sleet showers
                        13: "sleet", # Moderate sleet showers
                        14: "sleet", # Heavy sleet showers
                        15: "climacell_snow_light", # Light snow showers
                        16: "snow", # Moderate snow showers
                        17: "snow", # Heavy snow showers
                        18: 'climacell_rain_light' if is_daytime else 'rain_night_light', # Light rain
                        19: "climacell_rain" if is_daytime else "rain_night", # Moderate rain
                        20: "climacell_rain_heavy" if is_daytime else "rain_night_heavy", # Heavy rain
                        21: "thundershower_rain", # Thunder
                        22: "sleet", # Light sleet
                        23: "sleet", # Moderate sleet
                        24: "sleet", # Heavy sleet
                        25: "climacell_snow_light", # Light snowfall
                        26: "snow", # Moderate snowfall
                        27: "snow", # Heavy snowfall
                    }

        icon = icon_dict[weathercode]
        logging.debug(
            "get_icon_by_weathercode({}) - {}"
            .format(weathercode, icon))

        return icon

    def get_description_from_smhi_weathercode(self, weathercode):
        description_dict = {
                        1: "Clear sky",
                        2: "Nearly clear sky",
                        3: "Variable cloudiness",
                        4: "Halfclear sky",
                        5: "Cloudy sky",
                        6: "Overcast",
                        7: "Fog",
                        8: "Light rain showers",
                        9: "Moderate rain showers",
                        10: "Heavy rain showers",
                        11: "Thunderstorm",
                        12: "Light sleet showers",
                        13: "Moderate sleet showers",
                        14: "Heavy sleet showers",
                        15: "Light snow showers",
                        16: "Moderate snow showers",
                        17: "Heavy snow showers",
                        18: "Light rain",
                        19: "Moderate rain",
                        20: "Heavy rain",
                        21: "Thunder",
                        22: "Light sleet",
                        23: "Moderate sleet",
                        24: "Heavy sleet",
                        25: "Light snowfall",
                        26: "Moderate snowfall",
                        27: "Heavy snowfall",
                    }
        description = description_dict[weathercode]

        logging.debug(
            "get_description_by_weathercode({}) - {}"
            .format(weathercode, description))

        return description.title()

    # Get weather from SMHI API
    # https://opendata.smhi.se/apidocs/metfcst/get-forecast.html#get-point-forecast
    # The API response is a complete forecast approximately 10 days ahead of the latest current forecast.
    # All times in the answer given in UTC.
    # Precipitation parameters have a distribution in time (a time interval) until the valid time for current data.
    # The interval starts at the time step before. At the beginning of the forecast, the interval is one hour.
    # Later in the forecast, the time interval increases (eg 3, 6 and 12 h). Unit remains mm / h.
    # So, current hour is index 0, next hour is index 1
    # The API accepts 6 decimals in the lon/lat. With more decimals, it returns 404.

    def get_weather(self):

        url = ("https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/{}/lat/{}/data.json"
               .format(self.location_long, self.location_lat))

        headers = {"User-Agent": self.smhi_self_id}

        response_data = self.get_response_json(url, headers=headers)
        logging.debug(response_data)
        weather_data = response_data["timeSeries"][0]["parameters"]
        logging.debug("get_weather() - {}".format(weather_data))

        # Get the weather code.
        if weather_data[18]["name"] == "Wsymb2":
            weather_code = weather_data[18]["values"][0]
        else:
            for data in weather_data:
                if data["name"] == "Wsymb2":
                    weather_code = data["values"][0]

        daytime = self.is_daytime(self.location_lat, self.location_long)

        # { "temperatureMin": "2.0", "temperatureMax": "15.1", "icon": "mostly_cloudy", "description": "Cloudy with light breezes" }
        # No Min or Max here. We just get the estimated temperature for the hour.
        # Since we get the forecast for several hours and days, maybe we could get the min/max for the XX hours?
        weather = {}
        weather["temperatureMin"] = weather_data[1]["values"][0]
        weather["temperatureMax"] = weather_data[1]["values"][0]
        weather["icon"] = self.get_icon_from_smhi_weathercode(weather_code, daytime)
        weather["description"] = self.get_description_from_smhi_weathercode(weather_code)
        logging.debug(weather)
        return weather
