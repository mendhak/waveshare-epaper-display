from alert_providers.base_provider import BaseAlertProvider
import logging

class MetEireannAlertProvider(BaseAlertProvider):
    '''
    Consume the Met Eireann JSON alert data; format described at
    https://www.met.ie/Open_Data/Warnings/Met_Eireann_Warning_description_June2020.pdf .
    '''

    def __init__(self, feed_url):
        self.feed_url = feed_url

    def get_alert(self):
        alert_data = self.get_response_json(self.feed_url)
        logging.debug("get_alert() - {}".format(alert_data))

        for item in alert_data:
            level = item["level"].capitalize()  	# "yellow" => "Yellow"
            # add the level to the description to make something like
            # "Yellow: Wind warning for Donegal, Leitrim, Mayo, Sligo"
            value = "%s: %s" % (level, item["headline"])
            return value

        return ""

# Since typically there is _not_ a weather warning in place, here's an example of what one looks like:
#
# [{
# "id": 1,
# "capId": "2.49.0.1.372.0.220405114905.N_Norm004_Weather",
# "type": "Wind",
# "severity": "Moderate",
# "certainty": "Likely",
# "level": "Yellow",
# "issued": "2022-04-05T12:49:05+01:00",
# "updated": "2022-04-05T12:49:05+01:00",
# "onset": "2022-04-06T13:00:00+01:00",
# "expiry": "2022-04-06T21:00:00+01:00",
# "headline": "Wind warning for Donegal, Leitrim, Mayo, Sligo",
# "description": "Very strong southwest winds veering northwest are expected on Wednesday afternoon and evening. Winds will be strongest at the coast with some severe gusts at times too, which may make driving conditions difficult. ",
# "regions": ["EI06"],
# "status": "Warning"
# }]
