#!/usr/bin/env python3
"""
Convert env.sh to config.toml format.
Run this to see what the config.toml would look like. Copy paste it to config.toml to use it:
.venv/bin/python3 migrate-env-to-toml.py

Run this to generate a config.toml file:
.venv/bin/python3 migrate-env-to-toml.py > config.toml
"""

import re
import os
import sys


def parse_env_sh(path):
    settings = {}
    if not os.path.exists(path):
        return settings
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m = re.match(r'^export\s+(\w+)\s*=\s*["\']?([^"\']*)["\']?$', line)
            if m:
                settings[m.group(1)] = m.group(2)
    return settings


def get_weather_provider(settings):
    mapping = {
        'CLIMACELL_APIKEY': 'climacell',
        'OPENWEATHERMAP_APIKEY': 'openweathermap',
        'METOFFICEDATAHUB_API_KEY': 'metoffice',
        'ACCUWEATHER_APIKEY': 'accuweather',
        'WEATHER_MET_EIREANN': 'met_eireann',
        'METNO_SELF_IDENTIFICATION': 'metno',
        'WEATHERGOV_SELF_IDENTIFICATION': 'weathergov',
        'SMHI_SELF_IDENTIFICATION': 'smhi',
    }
    for var, provider in mapping.items():
        if var in settings:
            return provider
    return 'metoffice'


def get_alert_provider(settings):
    mapping = {
        'ALERT_METOFFICE_FEED_URL': 'metoffice',
        'ALERT_MET_EIREANN_FEED_URL': 'met_eireann',
        'ALERT_WEATHERGOV_SELF_IDENTIFICATION': 'weathergov',
    }
    for var, provider in mapping.items():
        if var in settings:
            return provider
    return None


def escape_toml_string(s):
    return s.replace('\\', '\\\\').replace('"', '\\"')


def generate_toml(settings):
    lines = []
    weather_provider = get_weather_provider(settings)
    alert_provider = get_alert_provider(settings)



    # Display
    layout = settings.get('SCREEN_LAYOUT', '1')
    version = settings.get('WAVESHARE_EPD75_VERSION', '2')
    lines.append('[display]')
    lines.append(f'screen_output_layout = "{layout}"')
    lines.append(f'waveshare_epd75_version = "{version}"')
    lines.append('')

    # Weather
    lat = settings.get('WEATHER_LATITUDE', '51.5077')
    lon = settings.get('WEATHER_LONGITUDE', '-0.1277')
    fmt = settings.get('WEATHER_FORMAT', 'CELSIUS')
    ttl = settings.get('WEATHER_TTL', '3600')
    lines.append('[weather]')
    lines.append(f'provider = "{weather_provider}"')
    lines.append(f'latitude = "{escape_toml_string(lat)}"')
    lines.append(f'longitude = "{escape_toml_string(lon)}"')
    lines.append(f'format = "{fmt}"')
    lines.append(f'cache_ttl_seconds = {ttl}')
    lines.append('')

    # Weather provider config (only active one)
    lines.append(f'[weather.providers.{weather_provider}]')
    if weather_provider == 'metoffice':
        if 'METOFFICEDATAHUB_API_KEY' in settings:
            lines.append(f'api_key = "{escape_toml_string(settings["METOFFICEDATAHUB_API_KEY"])}"')
    elif weather_provider == 'openweathermap':
        if 'OPENWEATHERMAP_APIKEY' in settings:
            lines.append(f'api_key = "{escape_toml_string(settings["OPENWEATHERMAP_APIKEY"])}"')
    elif weather_provider == 'climacell':
        if 'CLIMACELL_APIKEY' in settings:
            lines.append(f'api_key = "{escape_toml_string(settings["CLIMACELL_APIKEY"])}"')
    elif weather_provider == 'accuweather':
        if 'ACCUWEATHER_APIKEY' in settings:
            lines.append(f'api_key = "{escape_toml_string(settings["ACCUWEATHER_APIKEY"])}"')
        if 'ACCUWEATHER_LOCATIONKEY' in settings:
            lines.append(f'location_key = "{escape_toml_string(settings["ACCUWEATHER_LOCATIONKEY"])}"')
    elif weather_provider == 'metno':
        if 'METNO_SELF_IDENTIFICATION' in settings:
            lines.append(f'self_identification = "{escape_toml_string(settings["METNO_SELF_IDENTIFICATION"])}"')
    elif weather_provider == 'weathergov':
        if 'WEATHERGOV_SELF_IDENTIFICATION' in settings:
            lines.append(f'self_identification = "{escape_toml_string(settings["WEATHERGOV_SELF_IDENTIFICATION"])}"')
    elif weather_provider == 'smhi':
        if 'SMHI_SELF_IDENTIFICATION' in settings:
            lines.append(f'self_identification = "{escape_toml_string(settings["SMHI_SELF_IDENTIFICATION"])}"')
    elif weather_provider == 'met_eireann':
        pass  # No config needed
    lines.append('')

    # Calendar
    cal_ttl = settings.get('CALENDAR_TTL', '3600')
    include_past = settings.get('CALENDAR_INCLUDE_PAST_EVENTS_FOR_TODAY', '0')
    lines.append('[calendar]')
    lines.append('max_events = 10')
    lines.append(f'cache_ttl_seconds = {cal_ttl}')
    lines.append(f'include_past_events_for_today = {str(include_past == "1").lower()}')
    lines.append('')

    # Calendar providers (only active ones)
    if 'GOOGLE_CALENDAR_ID' in settings:
        lines.append('[[calendar.providers.google]]')
        lines.append(f'id = "{escape_toml_string(settings["GOOGLE_CALENDAR_ID"])}"')
        if 'GOOGLE_CALENDAR_TIME_ZONE_NAME' in settings:
            lines.append(f'time_zone = "{escape_toml_string(settings["GOOGLE_CALENDAR_TIME_ZONE_NAME"])}"')
        lines.append('enabled = true')
        lines.append('')

    if 'OUTLOOK_CALENDAR_ID' in settings:
        lines.append('[[calendar.providers.outlook]]')
        lines.append(f'calendar_id = "{escape_toml_string(settings["OUTLOOK_CALENDAR_ID"])}"')
        lines.append('enabled = true')
        lines.append('')

    if 'ICS_CALENDAR_URL' in settings:
        lines.append('[[calendar.providers.ics]]')
        lines.append(f'url = "{escape_toml_string(settings["ICS_CALENDAR_URL"])}"')
        lines.append('enabled = true')
        lines.append('')

    if 'CALDAV_CALENDAR_URL' in settings:
        lines.append('[[calendar.providers.caldav]]')
        lines.append(f'url = "{escape_toml_string(settings["CALDAV_CALENDAR_URL"])}"')
        if 'CALDAV_USERNAME' in settings:
            lines.append(f'username = "{escape_toml_string(settings["CALDAV_USERNAME"])}"')
        if 'CALDAV_PASSWORD' in settings:
            lines.append(f'password = "{escape_toml_string(settings["CALDAV_PASSWORD"])}"')
        if 'CALDAV_CALENDAR_ID' in settings:
            lines.append(f'id = "{escape_toml_string(settings["CALDAV_CALENDAR_ID"])}"')
        lines.append('enabled = true')
        lines.append('')

    # Alerts
    lines.append('[alerts]')
    if alert_provider:
        alert_ttl = settings.get('ALERT_TTL', '3600')
        lines.append(f'provider = "{alert_provider}"')
        lines.append(f'cache_ttl_seconds = {alert_ttl}')
        lines.append('')
        lines.append(f'[alerts.providers.{alert_provider}]')
        if alert_provider == 'metoffice' and 'ALERT_METOFFICE_FEED_URL' in settings:
            lines.append(f'feed_url = "{escape_toml_string(settings["ALERT_METOFFICE_FEED_URL"])}"')
        elif alert_provider == 'met_eireann' and 'ALERT_MET_EIREANN_FEED_URL' in settings:
            lines.append(f'feed_url = "{escape_toml_string(settings["ALERT_MET_EIREANN_FEED_URL"])}"')
        elif alert_provider == 'weathergov' and 'ALERT_WEATHERGOV_SELF_IDENTIFICATION' in settings:
            lines.append(f'self_identification = "{escape_toml_string(settings["ALERT_WEATHERGOV_SELF_IDENTIFICATION"])}"')
    else:
        lines.append('# provider = "metoffice"')
        lines.append('# cache_ttl_seconds = 3600')
    lines.append('')


    # Privacy
    xkcd = settings.get('PRIVACY_MODE_XKCD', '0')
    lit = settings.get('PRIVACY_MODE_LITERATURE_CLOCK', '0')
    lines.append('[privacy]')
    lines.append(f'xkcd = {str(xkcd == "1").lower()}')
    lines.append(f'literature_clock = {str(lit == "1").lower()}')
    lines.append('')

    # Locale
    lang = settings.get('LANG', 'en_US.UTF-8')
    log_level = settings.get('LOG_LEVEL', 'INFO')
    lines.append('[locale]')
    lines.append(f'language = "{escape_toml_string(lang)}"')
    lines.append(f'log_level = "{escape_toml_string(log_level)}"')
    lines.append('')


    return '\n'.join(lines)


def main():
    if not os.path.exists('env.sh'):
        print('No env.sh found', file=sys.stderr)
        sys.exit(1)

    settings = parse_env_sh('env.sh')
    if not settings:
        print('No active settings in env.sh (all commented out)', file=sys.stderr)
        sys.exit(1)

    print(generate_toml(settings))


if __name__ == '__main__':
    main()
