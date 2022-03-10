import logging
import datetime
from weather_providers.base_provider import BaseWeatherProvider


class MetOffice(BaseWeatherProvider):
    def __init__(self, metoffice_clientid, metoffice_clientsecret, location_lat, location_long, units):
        self.metoffice_clientid = metoffice_clientid
        self.metoffice_clientsecret = metoffice_clientsecret
        self.location_lat = location_lat
        self.location_long = location_long
        self.units = units

    # Map MetOffice icons to local icons
    # Reference: https://www.metoffice.gov.uk/services/data/datapoint/code-definitions
    def get_icon_from_metoffice_weathercode(self, weathercode, is_daytime):

        icon_dict = {
                        0: "clearnight",  # Clear night
                        1: "clear_sky_day",  # Sunny day
                        2: "partlycloudynight",  # Partly cloudy (night)
                        3: "scattered_clouds",  # Partly cloudy (day)
                        4: "",  # Not used
                        5: "haze",  # Mist
                        6: "climacell_fog",  # Fog
                        7: "mostly_cloudy" if is_daytime else "mostly_cloudy_night",  # Cloudy
                        8: "overcast",  # Overcast
                        9: "rain_night_light",  # Light rain shower (night)
                        10: "climacell_rain_light",  # Light rain shower (day)
                        11: "climacell_drizzle",  # Drizzle
                        12: "climacell_rain_light",  # Light rain
                        13: "rain_night_heavy",  # Heavy rain shower (night)
                        14: "climacell_rain_heavy",  # Heavy rain shower (day)
                        15: "climacell_rain_heavy",  # Heavy rain
                        16: "sleet",  # Sleet shower (night)
                        17: "sleet",  # Sleet shower (day)
                        18: "sleet",  # Sleet
                        19: "climacell_ice_pellets",  # Hail shower (night)
                        20: "climacell_ice_pellets",  # Hail shower (day)
                        21: "climacell_ice_pellets_heavy",  # Hail
                        22: "climacell_snow_light",  # Light snow shower (night)
                        23: "climacell_snow_light",  # Light snow shower (day)
                        24: "climacell_snow_light",  # Light snow
                        25: "snow",  # Heavy snow shower (night)
                        26: "snow",  # Heavy snow shower (day)
                        27: "snow",  # Heavy snow
                        28: "thundershower_rain",  # Thunder shower (night)
                        29: "thundershower_rain",  # Thunder shower (day)
                        30: "thundershower_rain",  # Thunder
                    }

        icon = icon_dict[weathercode]
        logging.debug(
            "get_icon_by_weathercode({}) - {}"
            .format(weathercode, icon))

        return icon

    def get_description_from_metoffice_weathercode(self, weathercode):
        description_dict = {
                                0: "Clear night",
                                1: "Sunny day",
                                2: "Partly cloudy",
                                3: "Partly cloudy",
                                4: "Not used",
                                5: "Mist",
                                6: "Fog",
                                7: "Cloudy",
                                8: "Overcast",
                                9: "Light rain shower",
                                10: "Light rain shower",
                                11: "Drizzle",
                                12: "Light rain",
                                13: "Heavy rain shower",
                                14: "Heavy rain shower",
                                15: "Heavy rain",
                                16: "Sleet shower",
                                17: "Sleet shower",
                                18: "Sleet",
                                19: "Hail shower",
                                20: "Hail shower",
                                21: "Hail",
                                22: "Light snow shower",
                                23: "Light snow shower",
                                24: "Light snow",
                                25: "Heavy snow shower",
                                26: "Heavy snow shower",
                                27: "Heavy snow",
                                28: "Thunder shower",
                                29: "Thunder shower",
                                30: "Thunder",
                            }
        description = description_dict[weathercode]

        logging.debug(
            "get_description_by_weathercode({}) - {}"
            .format(weathercode, description))

        return description.title()

    # Get weather from MetOffice Weather DataHub
    # https://metoffice.apiconnect.ibmcloud.com/metoffice/production/node/173
    def get_weather(self):

        url = ("https://api-metoffice.apiconnect.ibmcloud.com/metoffice/production/v0/forecasts/point/daily?excludeParameterMetadata=false&includeLocationName=false&latitude={}&longitude={}"
               .format(self.location_lat, self.location_long))

        headers = {
            "X-IBM-Client-Id": self.metoffice_clientid,
            "X-IBM-Client-Secret": self.metoffice_clientsecret,
            "accept": "application/json"
        }

        response_data = self.get_response_json(url, headers=headers)
        logging.debug(response_data)

        datahub_time = datetime.datetime.now().strftime("%Y-%m-%dT00:00Z")  # midnight of the current day

        for day_forecast in response_data["features"][0]["properties"]["timeSeries"]:
            if day_forecast["time"] == datahub_time:
                weather_data = day_forecast

        logging.debug("get_weather() - {}".format(weather_data))

        daytime = self.is_daytime(self.location_lat, self.location_long)
        weather_code = weather_data["daySignificantWeatherCode"] if daytime else weather_data["nightSignificantWeatherCode"]
        # { "temperatureMin": "2.0", "temperatureMax": "15.1", "icon": "mostly_cloudy", "description": "Cloudy with light breezes" }
        weather = {}
        weather["temperatureMin"] = weather_data["nightMinScreenTemperature"] if self.units == "metric" else self.c_to_f(weather_data["nightMinScreenTemperature"])
        weather["temperatureMax"] = weather_data["dayMaxScreenTemperature"] if self.units == "metric" else self.c_to_f(weather_data["dayMaxScreenTemperature"])
        weather["icon"] = self.get_icon_from_metoffice_weathercode(weather_code, daytime)
        weather["description"] = self.get_description_from_metoffice_weathercode(weather_code)
        logging.debug(weather)
        return weather
