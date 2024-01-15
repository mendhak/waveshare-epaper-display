import datetime
import os.path
import os
import logging
from utility import update_svg, configure_logging

configure_logging()

inky_width = int(os.getenv('INKY_DISPLAY_WIDTH', None))
inky_height = int(os.getenv("INKY_DISPLAY_HEIGHT", None))

svg_width = 800
svg_height = int(inky_height * svg_width / inky_width)

def main():
  output_svg_filename = 'screen-output-weather.svg'
  logging.info(f'resize svg to {svg_width}x{svg_height}')
  output_dict = {
    "480": str(svg_height)
  }
  update_svg(output_svg_filename, output_svg_filename, output_dict)


if __name__ == "__main__":
    main()
