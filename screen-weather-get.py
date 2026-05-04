#!/usr/bin/python

import datetime
import sys
import logging
import json
from weather_providers import climacell, openweathermap, metofficedatahub, metno, meteireann, accuweather, visualcrossing, weathergov, smhi
from alert_providers import metofficerssfeed, weathergovalerts
from alert_providers import meteireann as meteireannalertprovider
from utility import get_formatted_time, update_svg, configure_logging, configure_locale, is_stale
import textwrap
import html
import tomllib

with open("config.toml", "rb") as f:
    config = tomllib.load(f)

configure_locale()
configure_logging(config["locale"]["log_level"])


def format_weather_description(weather_description):
    if len(weather_description) < 20:
        return {'1': weather_description, '2': ''}

    splits = textwrap.fill(weather_description, 20, break_long_words=False,
                           max_lines=2, placeholder='...').split('\n')
    weather_dict = {'1': splits[0]}
    weather_dict['2'] = splits[1] if len(splits) > 1 else ''
    return weather_dict


def get_weather(location_lat, location_long, units, weather_provider_name, provider_config):

    api_key = provider_config.get("api_key", None)
    location_key = provider_config.get("location_key", None)
    self_identification = provider_config.get("self_identification", None)

    match weather_provider_name:
        case "visualcrossing":
            logging.info("Getting weather from Visual Crossing")
            if not api_key:
                logging.error("Visual Crossing API key not configured.")
                sys.exit(1)
            weather_provider = visualcrossing.VisualCrossing(api_key, location_lat, location_long, units)
        case "met_eireann":
            logging.info("Getting weather from Met Eireann")
            weather_provider = meteireann.MetEireann(location_lat, location_long, units)
        case "weathergov":
            logging.info("Getting weather from Weather.gov")
            if not self_identification:
                logging.error("Weather.gov self identification not configured.")
                sys.exit(1)
            weather_provider = weathergov.WeatherGov(self_identification, location_lat, location_long, units)
        case "metno":
            logging.info("Getting weather from Met.no")
            if not self_identification:
                logging.error("Met.no self identification not configured.")
                sys.exit(1)
            weather_provider = metno.MetNo(self_identification, location_lat, location_long, units)
        case "accuweather":
            logging.info("Getting weather from Accuweather")
            if not api_key or not location_key:
                logging.error("AccuWeather API key or location key not configured.")
                sys.exit(1)
            weather_provider = accuweather.AccuWeather(api_key, location_lat,
                                                       location_long,
                                                       location_key,
                                                       units)
        case "metoffice":
            logging.info("Getting weather from Met Office Weather Datahub")
            if not api_key:
                logging.error("Met Office Weather Datahub API key not configured.")
                sys.exit(1)
            weather_provider = metofficedatahub.MetOffice(api_key,
                                                          location_lat,
                                                          location_long,
                                                          units)
        case "openweathermap":
            logging.info("Getting weather from OpenWeatherMap")
            if not api_key:
                logging.error("OpenWeatherMap API key not configured.")
                sys.exit(1)
            weather_provider = openweathermap.OpenWeatherMap(api_key,
                                                             location_lat,
                                                             location_long,
                                                             units)
        case "climacell":
            logging.info("Getting weather from Climacell")
            if not api_key:
                logging.error("Climacell API key not configured.")
                sys.exit(1)
            weather_provider = climacell.Climacell(api_key, location_lat, location_long, units)
        case "smhi":
            logging.info("Getting weather from SMHI")
            if not self_identification:
                logging.error("SMHI self identification not configured.")
                sys.exit(1)
            weather_provider = smhi.SMHI(self_identification, location_lat, location_long, units)
        case _:
            logging.error(f"Unsupported weather provider: {weather_provider_name}")
            sys.exit(1)

    weather = weather_provider.get_weather()
    logging.info("weather - {}".format(weather))
    return weather


def format_alert_description(alert_message):
    return html.escape(alert_message)


def get_alert_message(location_lat, location_long, alerts_provider_name, alerts_config):
    alert_message = ""

    feed_url = alerts_config.get("feed_url", None)
    self_identification = alerts_config.get("self_identification", None)

    match alerts_provider_name:
        case "weathergov":
            logging.info("Getting weather alert from Weather.gov API")
            if not self_identification:
                logging.error("Weather.gov self identification not configured.")
                sys.exit(1)
            alert_provider = weathergovalerts.WeatherGovAlerts(location_lat, location_long, self_identification)
            alert_message = alert_provider.get_alert()
        case "metoffice":
            logging.info("Getting weather alert from Met Office RSS Feed")
            if not feed_url:
                logging.error("Met Office RSS feed URL not configured.")
                sys.exit(1)
            alert_provider = metofficerssfeed.MetOfficeRssFeed(feed_url)
            alert_message = alert_provider.get_alert()
        case "met_eireann":
            logging.info("Getting weather alert from Met Eireann")
            if not feed_url:
                logging.error("Met Eireann feed URL not configured.")
                sys.exit(1)
            alert_provider = meteireannalertprovider.MetEireannAlertProvider(feed_url)
            alert_message = alert_provider.get_alert()
        case _:
            logging.error(f"Unsupported alert provider: {alerts_provider_name}")
            sys.exit(1)

    logging.info("alert - {}".format(alert_message))
    return alert_message


def fetch_weather(location_lat, location_long, units, weather_provider_name, provider_config):
    weather_ttl = float(config["weather"].get("cache_ttl_seconds", 3600))
    cache_file = 'cache_weather.json'

    if is_stale(cache_file, weather_ttl):
        logging.info("Cache is stale, fetching fresh weather data")
        weather = get_weather(location_lat, location_long, units, weather_provider_name, provider_config)
        if not weather:
            logging.error("Unable to fetch weather payload. SVG will not be updated.")
            return None, None
        weather_desc = format_weather_description(weather["description"])

        with open(cache_file, 'w') as f:
            json.dump({"weather": weather, "weather_desc": weather_desc}, f)
        logging.info("Saved weather data to cache")
        return weather, weather_desc
    else:
        logging.info("Using cached weather data")
        with open(cache_file, 'r') as f:
            cache_data = json.load(f)
        return cache_data["weather"], cache_data["weather_desc"]


def fetch_alert(location_lat, location_long, alerts_provider_name, alerts_config):
    alerts_ttl = float(config["alerts"].get("cache_ttl_seconds", 3600))
    cache_file = 'cache_alerts.json'

    if is_stale(cache_file, alerts_ttl):
        logging.info("Cache is stale, fetching fresh alert data")
        alert_message = get_alert_message(location_lat, location_long, alerts_provider_name, alerts_config)
        alert_message = format_alert_description(alert_message)

        with open(cache_file, 'w') as f:
            json.dump({"alert_message": alert_message}, f)
        logging.info("Saved alert data to cache")
        return alert_message
    else:
        logging.info("Using cached alert data")
        with open(cache_file, 'r') as f:
            return json.load(f)["alert_message"]


def main():

    weather_provider_name = config["weather"]["provider"]

    if not weather_provider_name:
        logging.error("No weather provider configured. Please set the 'provider' field in the config.toml file.")
        sys.exit(1)
    else:
        logging.info(f"Selected weather provider: {weather_provider_name}")

    provider_config = config["weather"]["providers"][weather_provider_name]

    location_lat = config["weather"].get("latitude", "51.5077")
    location_long = config["weather"].get("longitude", "-0.1277")
    weather_format = config["weather"].get("format", "CELSIUS")

    if (weather_format == "CELSIUS"):
        units = "metric"
        degrees = "°C"
    else:
        units = "imperial"
        degrees = "°F"

    weather, weather_desc = fetch_weather(location_lat, location_long, units, weather_provider_name, provider_config)
    if weather is None:
        logging.error("Unable to fetch weather data")
        return

    logging.debug(f"Fetched weather: {weather}")
    logging.debug(f"Fetched weather description: {weather_desc}")

    alerts_enabled = config["alerts"].get("enabled", False)
    alert_message = ""
    if alerts_enabled:
        alerts_provider_name = config["alerts"].get("provider", None)

        if alerts_provider_name:
            logging.info(f"Selected alert provider: {alerts_provider_name}")
            alerts_config = config["alerts"]["providers"].get(alerts_provider_name, None)

            if alerts_config:
                alert_message = fetch_alert(location_lat, location_long, alerts_provider_name, alerts_config)
            else:
                logging.error(f"Alert provider '{alerts_provider_name}' is not configured in the config.toml file.")

        logging.debug(f"Fetched alert message: {alert_message}")

    template_name = config["display"].get("screen_output_layout", "1")

    time_now = get_formatted_time(datetime.datetime.now())
    time_now_font_size = "100px"

    if len(time_now) > 6:
        time_now_font_size = str(100 - (len(time_now)-5) * 5) + "px"

    output_dict = {
        'LOW_ONE': "{}{}".format(str(round(weather['temperatureMin'])), degrees),
        'HIGH_ONE': "{}{}".format(str(round(weather['temperatureMax'])), degrees),
        'ICON_ONE': weather["icon"],
        'WEATHER_DESC_1': weather_desc['1'],
        'WEATHER_DESC_2': weather_desc['2'],
        'TIME_NOW_FONT_SIZE': time_now_font_size,
        'TIME_NOW': time_now,
        'HOUR_NOW': datetime.datetime.now().strftime("%-I %p"),
        'DAY_ONE': datetime.datetime.now().strftime("%b %-d, %Y"),
        'DAY_NAME': datetime.datetime.now().strftime("%A"),
        'ALERT_MESSAGE_VISIBILITY': "visible" if alert_message else "hidden",
        'ALERT_MESSAGE': alert_message
    }

    logging.info(output_dict)

    logging.info("Updating SVG")

    template_svg_filename = f'screen-template.{template_name}.svg'
    output_svg_filename = 'screen-output-weather.svg'
    update_svg(template_svg_filename, output_svg_filename, output_dict)


if __name__ == "__main__":
    main()
