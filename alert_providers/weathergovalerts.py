from alert_providers.base_provider import BaseAlertProvider
import logging
import xml.etree.ElementTree as ET

class WeatherGovAlerts(BaseAlertProvider):
    def __init__(self, location_lat, location_long, weathergov_self_id):
        self.location_lat = location_lat
        self.location_long = location_long
        self.weathergov_self_id = weathergov_self_id


    def get_alert(self):
        try:
            severe = self.get_response_json("https://api.weather.gov/alerts?point={},{}".format(self.location_lat, self.location_long), 
                                            headers={'User-Agent':'({0})'.format(self.weathergov_self_id)})
            logging.debug("get_alert - {}".format(severe))
            if 'features' in severe:
                if 'properties' in severe["features"][0]:
                    if 'parameters' in severe["features"][0]["properties"]:
                        if 'NWSheadline' in severe["features"][0]["properties"]["parameters"]:
                            return severe["features"][0]["properties"]["parameters"]["NWSheadline"][0]
        except Exception as error:
            pass
        return ""
        
