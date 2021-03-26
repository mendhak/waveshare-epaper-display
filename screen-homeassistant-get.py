# Scrape sensor values from a local HomeAssistant instance.

from __future__ import print_function
import codecs
import os
import requests
import json

template = 'screen-output-weather.svg'

authorization_token = os.getenv("HASS_BEARER_TOKEN","")
hass_url = os.getenv("HASS_URL", "http://localhost:8123/")
sensors = json.loads(os.getenv("HASS_SENSORS", "{}"))

auth_headers = {
    'Authorization': 'Bearer ' + authorization_token,
    'Content-Type': 'application/json'
}

output = codecs.open(template , 'r', encoding='utf-8').read()
charge_icon = "\N{high voltage sign}"

for sensor in sensors:
  r = requests.get(hass_url + 'api/states/' + sensor,
	  headers=auth_headers)
  print(r.text)

  j = json.loads(r.text)

  if "binary_sensor" in sensor:
    val = j["state"]
    if "on" in val:
      val = charge_icon
    else:
      val = ""

  else:
    val = str(int(j["state"]))
    # support this weird API for MercedesME: https://community.home-assistant.io/t/mercedes-me-component/41911/590
    if "chargingactive" in j and "chargingstatus" in j:
      if int(j["chargingstatus"]) in [0,1]:
        val = val + charge_icon

  output = output.replace(sensors[sensor], val)
  print(sensor + ": " + val)

codecs.open('screen-output-homeassistant.svg', 'w', encoding='utf-8').write(output)

