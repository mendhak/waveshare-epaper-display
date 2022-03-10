import logging
import datetime
from weather_providers.base_provider import BaseWeatherProvider


class VisualCrossing(BaseWeatherProvider):
    def __init__(self, visualcrossing_apikey, location_lat, location_long, units):
        self.visualcrossing_apikey = visualcrossing_apikey
        self.location_lat = location_lat
        self.location_long = location_long
        self.units = units

    # Map VisualCrossing icons to local icons
    # Reference: https://www.visualcrossing.com/resources/documentation/weather-api/defining-icon-set-in-the-weather-api/
    def get_icon_from_visualcrossing_weathercode(self, weathercode, is_daytime):

        icon_dict = {
                    "snow": "snow",  # Amount of snow is greater than zero
                    "rain": "climacell_rain_light" if is_daytime else "rain_night_light",  # Amount of rainfall is greater than zero
                    "fog": "climacell_fog",  # Visibility is low (lower than one kilometer or mile)
                    "wind": "wind",  # Wind speed is high (greater than 30 kph or mph)
                    "cloudy": "mostly_cloudy" if is_daytime else "mostly_cloudy_night",  # Cloud cover is greater than 75% cover
                    "partly-cloudy-day": "scattered_clouds" if is_daytime else "partlycloudynight",  # Cloud cover is greater than 25% cover during day time.
                    "partly-cloudy-night": "partlycloudynight",  # Cloud cover is greater than 25% cover during night time.
                    "clear-day": "clear_sky_day" if is_daytime else "clearnight",  # Cloud cover is less than 25% cover during day time
                    "clear-night": "clearnight"  # Cloud cover is less than 25% cover during day time
                    }

        icon = icon_dict[weathercode]
        logging.debug(
            "get_icon_by_weathercode({}, {}) - {}"
            .format(weathercode, is_daytime, icon))

        return icon

    # Get weather from VisualCrossing Timeline API
    # https://www.visualcrossing.com/resources/documentation/weather-api/timeline-weather-api/
    def get_weather(self):

        url = ("https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{},{}?unitGroup={}&key={}&include=fcst,alerts"
               .format(self.location_lat, self.location_long, "us" if self.units != "metric" else "metric", self.visualcrossing_apikey))

        response_data = self.get_response_json(url)

        current_day = datetime.datetime.now().strftime("%Y-%m-%d")

        for day_forecast in response_data["days"]:
            if day_forecast["datetime"] == current_day:
                weather_data = day_forecast

        logging.debug("get_weather() - {}".format(weather_data))

        daytime = self.is_daytime(self.location_lat, self.location_long)

        # { "temperatureMin": "2.0", "temperatureMax": "15.1", "icon": "mostly_cloudy", "description": "Cloudy with light breezes" }
        weather = {}
        weather["temperatureMin"] = weather_data["tempmin"]
        weather["temperatureMax"] = weather_data["tempmax"]
        weather["icon"] = self.get_icon_from_visualcrossing_weathercode(weather_data["icon"], daytime)
        weather["description"] = weather_data["description"]
        logging.debug(weather)
        return weather
