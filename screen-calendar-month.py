import calendar
import datetime
import os.path
import os
import logging
from utility import get_formatted_time, update_svg, configure_logging, get_formatted_date, configure_locale

configure_locale()
configure_logging()

def get_formatted_calendar_month() -> dict:
    formatted_calendar_month = {}
    today = datetime.date.today()
    firstWeekDay, days = calendar.monthrange(today.year, today.month)
    for d in range(37):
        if d < firstWeekDay or d >= firstWeekDay + days:
            formatted_calendar_month[f'D{d:0>{2}}'] = ""
        else:
            formatted_calendar_month[f'D{d:0>{2}}'] = f'{d - firstWeekDay + 1}'
            if d - firstWeekDay + 1 == today.day:
                formatted_calendar_month[f'C{d:0>{2}}'] = "important"
    return formatted_calendar_month


def main():
    output_svg_filename = 'screen-output-weather.svg'

    output_dict = get_formatted_calendar_month()

    logging.info("main() - {}".format(output_dict))

    logging.info("Updating SVG")
    update_svg(output_svg_filename, output_svg_filename, output_dict)


if __name__ == "__main__":
    main()
