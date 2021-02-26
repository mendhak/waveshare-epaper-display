#!/usr/bin/python3
import sys
import os
libdir = "./lib/e-Paper/RaspberryPi_JetsonNano/python/lib"
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
import datetime
from PIL import Image

logging.basicConfig(level=logging.INFO)

if (os.getenv("WAVESHARE_EPD75_VERSION", "2") == "1"):
    from waveshare_epd import epd7in5 as epd7in5
else:
    from waveshare_epd import epd7in5b_V2 as epd7in5

try:
    epd = epd7in5.EPD()
    logging.debug("Initialize screen")
    epd.init()

    # Always do a full refresh
    epd.Clear()

    #Full screen refresh at 2 AM
    # if datetime.datetime.now().minute==0 and datetime.datetime.now().hour==2:
        # logging.debug("Clear screen")
        # epd.Clear()

    logging.debug("Read image files")
    black_image = Image.open(sys.argv[1])
    red_image = Image.open(sys.argv[2])

    logging.info("Display image file on screen")
    epd.display(epd.getbuffer(black_image), epd.getbuffer(red_image))
    epd.sleep()
    epd.Dev_exit()

except IOError as e:
    logging.exception(e)

except KeyboardInterrupt:
    logging.debug("Keyboard Interrupt - Exit")
    epd7in5.epdconfig.module_exit()
    exit()
