#!/usr/bin/python
# -*- coding:utf-8 -*-

import epd7in5
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

try:
    epd = epd7in5.EPD()
    epd.init()
    print("Clear")
    epd.Clear(0xFF)
    
    # print("read image file")
    # start=time.time()
    # image = Image.new('1', (epd7in5.EPD_WIDTH, epd7in5.EPD_HEIGHT), 255)  # 255: clear the frame
    # draw = ImageDraw.Draw(image)
    # image = Image.open('weather-script-output.png')
    # epd.display(epd.getbuffer(image))
    # end=time.time()
    # print("That took " + str(end - start))
    # time.sleep(2)
     
    print("read bmp file on window")
    start=time.time()
    Himage2 = Image.new('1', (epd7in5.EPD_WIDTH, epd7in5.EPD_HEIGHT), 255)  # 255: clear the frame
    bmp = Image.open('screen-output.png')
    Himage2.paste(bmp, (0,0))
    epd.display(epd.getbuffer(Himage2))
    end=time.time()
    print("That took " + str(end - start))
    time.sleep(2)
        
    epd.sleep()
        
except:
    print('traceback.format_exc():\n%s', traceback.format_exc())
    exit()

