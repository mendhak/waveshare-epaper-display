import datetime
import calendar
import svgwrite
from utility import update_svg, configure_locale, configure_logging
import locale
import babel
import logging
from collections import deque


configure_logging()
configure_locale()

# Set the first weekday based on locale
# Handle UnknownLocaleError
try:
    babel_locale = babel.Locale(locale.getlocale()[0])
    logging.info(babel_locale)
except babel.core.UnknownLocaleError:
    logging.error("Could not get locale from environment. ")


calendar.setfirstweekday(babel_locale.first_week_day)

# Get current year and month
now = datetime.datetime.now()
current_year, current_month, current_day = now.year, now.month, now.day

# Get the month's calendar
cal = calendar.monthcalendar(current_year, current_month)

# Create a new SVG drawing
dwg = svgwrite.Drawing(profile='tiny')
dwg['transform'] = 'translate(500, 240)'
dwg['id'] = 'month-cal'

# Define dimensions
# cell_size = 40
cell_width = 40
cell_height = 30
width = 7 * cell_width
height = (len(cal) + 1) * cell_height

# Have the day abbreviations respect the locale's first day of the week
day_abbr = deque(list(calendar.day_abbr))
day_abbr.rotate(-calendar.firstweekday())

# Draw days of the week
for i, day in enumerate(day_abbr):
    dwg.add(dwg.text(day[:2], insert=(i*cell_width + 20, 20), fill='black'))

# Draw days of the month
for i, week in enumerate(cal):
    for j, day in enumerate(week):
        if day != 0:  # calendar.monthcalendar pads with 0s
            text = dwg.text(day, insert=(j*cell_width + 20, (i+2)*cell_height - 10), fill='black')
            if day == current_day:
                text['class'] = 'important'
            dwg.add(text)

logging.info(dwg.tostring())
update_svg('screen-output-weather.svg', 'screen-output-weather.svg', {'MONTH_CAL': dwg.tostring()})

# Don't save the SVG, it will write a file to disk.
