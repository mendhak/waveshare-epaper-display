# Scrape sensor values from a local HomeAssistant instance.

from __future__ import print_function
import codecs
import requests
import json

template = 'screen-output-weather.svg'

authorization_token = os.getenv("HASS_BEARER_TOKEN","")
hass_url = os.getenv("HASS_URL", "http://localhost:8123/")
sensors = json.load(os.getenv("HASS_SENSORS", "{}"))

auth_headers = {
    'Authorization': 'Bearer ' + authorization_token,
    'Content-Type': 'application/json'
}

output = codecs.open(template , 'r', encoding='utf-8').read()

for sensor in sensors:
  r = requests.get(hass_url + 'api/states/' + sensor,
	  headers=auth_headers)
  ## print(r.text)

  j = json.loads(r.text)
  val = int(j["state"])
  output = output.replace(sensors[sensor], str(val))
  print(sensor + ": " + str(val))

codecs.open('screen-output-homeassistant.svg', 'w', encoding='utf-8').write(output)

