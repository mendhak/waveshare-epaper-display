#!/usr/bin/python3
import sys
import os
import logging
import datetime
from PIL import Image
from utility import configure_logging

libdir = "./lib/e-Paper/RaspberryPi_JetsonNano/python/lib"
if os.path.exists(libdir):
    sys.path.append(libdir)

configure_logging()

if (os.getenv("WAVESHARE_EPD75_VERSION", "2") == "1"):
    from waveshare_epd import epd7in5 as epd7in5
else:
    from waveshare_epd import epd7in5_V2 as epd7in5

try:
    epd = epd7in5.EPD()
    logging.debug("Initialize screen")
    epd.init()

    # Full screen refresh at 2 AM
    if datetime.datetime.now().minute == 0 and datetime.datetime.now().hour == 2:
        logging.debug("Clear screen")
        epd.Clear()

    filename = sys.argv[1]

    logging.debug("Read image file: " + filename)
    Himage = Image.open(filename)
    logging.info("Display image file on screen")
    epd.display(epd.getbuffer(Himage))
    epd.sleep()
    epd.Dev_exit()

except IOError as e:
    logging.exception(e)

except KeyboardInterrupt:
    logging.debug("Keyboard Interrupt - Exit")
    epd7in5.epdconfig.module_exit()
    exit()
