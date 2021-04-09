# sCRAPE SENSOR VALUes from a local HomeAssistant instance.

from __future__ import print_function
import codecs
import os
import requests
import json
import logging

template = 'screen-output-weather.svg'

authorization_token = os.getenv("HASS_BEARER_TOKEN","")
hass_url = os.getenv("HASS_URL", "http://localhost:8123/")
sensors = json.loads(os.getenv("HASS_SENSORS", "{}"))

auth_headers = {
    'Authorization': 'Bearer ' + authorization_token,
    'Content-Type': 'application/json'
}

charge_icon = "\N{high voltage sign}"

logging.basicConfig(level=logging.DEBUG)

def scrape_sensors(output):
  for sensor in sensors:
    r = requests.get(hass_url + 'api/states/' + sensor,
	    headers=auth_headers)
    logging.debug("JSON response: " + r.text)
  
    j = json.loads(r.text)
    if "binary_sensor" in sensor:
      val = parse_binary_sensor(j)
    else:
      val = parse_sensor(j)
  
    output = output.replace(sensors[sensor], val)
    logging.info(sensor + ": " + val)
  return output

def parse_binary_sensor(j):
  try:
    val = j["state"]
    if "on" in val:
      return charge_icon
    else:
      return ""
  except:   # state not found; could be the sensor is unavailable
    return ""

def parse_sensor(j):
  try:
    val = str(int(j["state"]))
    # support this weird API for MercedesME: https://community.home-assistant.io/t/mercedes-me-component/41911/590
    if "attributes" in j:
      attrs = j["attributes"]
      if "chargingactive" in attrs and "chargingstatus" in attrs:
        if int(attrs["chargingstatus"]) in [0,1]:
          val = val + charge_icon
    return val

  except:   # casting to int failed, often because the value is the str literal "unavailable"
    return ""


output = codecs.open(template , 'r', encoding='utf-8').read()
if authorization_token != "":
  output = scrape_sensors(output)
codecs.open('screen-output-homeassistant.svg', 'w', encoding='utf-8').write(output)

