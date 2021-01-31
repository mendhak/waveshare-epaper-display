#!/usr/bin/python3
# -*- coding:utf-8 -*-
import sys
import os
#picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
#libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
libdir = "/home/pi/e-Paper/RaspberryPi_JetsonNano/python/lib"
if os.path.exists(libdir):
    print("Found")
    sys.path.append(libdir)

import logging

if os.getenv("WAVESHARE_EPD75_VERSION",1):
    from waveshare_epd import epd7in5 as epd7in5
else:
    from waveshare_epd import epd7in5_V2 as epd7in5


import time, datetime
from PIL import Image
import traceback

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd7in5 Demo")

    epd = epd7in5.EPD()
    logging.info("init and Clear")
    epd.init()
    
    #Full screen refresh at 2 AM
    if datetime.datetime.now().minute==0 and datetime.datetime.now().hour==2:
        epd.Clear()

    logging.info("3.read bmp file")
    #Himage = Image.open("/home/pi/waveshare-epaper-display/screen-output.bmp")
    Himage = Image.open(sys.argv[1])
    epd.display(epd.getbuffer(Himage))
    epd.sleep()
    epd.Dev_exit()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd7in5.epdconfig.module_exit()
    exit()
