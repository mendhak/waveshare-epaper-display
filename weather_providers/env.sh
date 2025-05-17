export WAVESHARE_EPD75_VERSION=2

export OPENWEATHERMAP_APIKEY=b3d2936da97dbce7940b4ecac4de8ce4

# Your latitude and longitude to pass to weather providers
export WEATHER_LATITUDE=-34.5493266
export WEATHER_LONGITUDE=-58.4601352

# Choose CELSIUS or FAHRENHEIT
export WEATHER_FORMAT=CELSIUS

# Pick a calendar provider
# Google Calendar ID, you can get this from Google Calendar Settings
#export GOOGLE_CALENDAR_ID=primary
# If your Google Calendar is a family calendar or doesn't allow setting timezones
# export GOOGLE_CALENDAR_TIME_ZONE_NAME=Asia/Kuala_Lumpur
# Or if you use Outlook Calendar, use python3 outlook_util.py to get available Calendar IDs
# export OUTLOOK_CALENDAR_ID=AQMkAxyz...
# Or if you use ICS Calendar,
export ICS_CALENDAR_URL=https://campus.ort.edu.ar/secundaria/belgrano/segundo-n/2025-ne2j/calendario/2189794/ical/
# Or if you have a CalDave calendar
# export CALDAV_CALENDAR_URL=https://nextcloud.example.com/remote.php/dav/principals/users/123456/
# export CALDAV_USERNAME=username
# export CALDAV_PASSWORD=password
# export CALDAV_CALENDAR_ID=xxxxxxxxxx

# Which layout to use. 1, 2, 3...
export SCREEN_LAYOUT=2

# Include all calendar events from today, even if they are past.
# export CALENDAR_INCLUDE_PAST_EVENTS_FOR_TODAY=1

# How long, in seconds, to cache weather for
export WEATHER_TTL=3600
# How long, in seconds, to cache the calendar for
export CALENDAR_TTL=3600

# Set a language, but ensure it's installed first. Run locale -a
# export LANG=ko_KR.UTF-8

# You can set this to DEBUG for troubleshooting, otherwise leave it at INFO.
export LOG_LEVEL=INFO

# Privacy mode. Just displays an XKCD comic instead.
export PRIVACY_MODE_XKCD=0
export PRIVACY_MODE_LITERATURE_CLOCK=0
