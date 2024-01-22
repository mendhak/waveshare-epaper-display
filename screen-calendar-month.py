import datetime
import calendar
from utility import update_svg, configure_locale, configure_logging
import locale
import babel
import logging
from collections import deque
import drawsvg as draw
import os

configure_logging()
configure_locale()

try:
    babel_locale = babel.Locale(locale.getlocale()[0])
    logging.debug(babel_locale)
except babel.core.UnknownLocaleError:
    logging.error("Could not get locale from environment. Using default locale.")
    babel_locale = babel.Locale("")


def main():
    logging.info("Generating SVG for calendar month")

    # Python does not know about the locale's first day of week 🤦  https://stackoverflow.com/a/4265852/974369
    # Use babel to set it instead
    calendar.setfirstweekday(babel_locale.first_week_day)

    now = datetime.datetime.now()
    current_year, current_month, current_day = now.year, now.month, now.day

    # Get this month's calendar as a matrix
    cal = calendar.monthcalendar(current_year, current_month)

    # Create a new SVG drawing
    top_left = os.getenv("MONTH_CALENDAR_TOP_LEFT", "(500, 240)")
    dwg = draw.Drawing(width=500, height=500, origin=(0,0),  id='month-cal', transform=f'translate{top_left}')

    cell_width = 40
    cell_height = 30

    # Have the day abbreviations respect the locale's first day of the week
    day_abbr = deque(list(calendar.day_abbr))
    day_abbr.rotate(-calendar.firstweekday())

    # Header for days of the week
    for i, day in enumerate(day_abbr):
        dwg.append(draw.Text(day[:2], font_size=None, x=i*cell_width + 20, y= 20, fill='black' ))

    # Days of the month per week
    for i, week in enumerate(cal):
        for j, day in enumerate(week):
            if day != 0:  # calendar.monthcalendar pads with 0s
                text_fill = 'black'
                if day == current_day:
                    text_fill = 'red'
                text = draw.Text(str(day), font_size=None, x=j*cell_width + 20, y=(i+2)*cell_height - 10, width=cell_width, height=cell_height, fill=text_fill)
                dwg.append(text)

    svg_output = dwg.as_svg()
    # Remove the <?xml> line
    svg_output = svg_output.split('\n', 1)[1]

    output_svg_filename = 'screen-output-weather.svg'
    output_dict = {'MONTH_CAL': svg_output}
    logging.info("main() - {}".format(output_dict))
    logging.info("Updating SVG")
    update_svg(output_svg_filename, output_svg_filename, output_dict)

if __name__ == "__main__":
    main()
