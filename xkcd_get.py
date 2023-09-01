import requests
import json
import wget
import logging
import os
import numpy as np
from PIL import Image


    

def xkcd_get_img():
    logging.info("Downloading xkcd-json")
    response = requests.get("https://xkcd.com/info.0.json")
    result = response.json()

    logging.info("Downloading xkcd_img")
    logging.info(result["img"])

    path = 'path/to/your/waveshare/implementation'
    filename = path + '/' + os.path.basename("xkcd-comic-strip.png")
    if os.path.exists(filename):
        os.remove(filename)
    wget.download(result["img"], "xkcd-comic-strip.png")
    
    # Convert grayscale to pseudo-rgb since grayscale confuses the eink display

    image = np.array(Image.open(filename).convert('RGB'))
    Image.fromarray(image).save('xkcd-comic-strip.png')


    """ If the downloaded image is too big to fit into the display downscale it
    while taking the scales into account.
    Afterwards resize the image to fit the screen. Sligh disortions can happen """
    
    im = Image.open(filename)
    logging.debug("Png size: ",im.size)
    if (im.size[0] > 800 and im.size[1] > 480):
        logging.debug("Picture is bigger than eink-display")
        print("After using thumbnail: ",im.size)
        im.thumbnail((800,480))

    if (im.size[0] < 800 and im.size[1] < 480):
        im = im.resize((800,480))
        logging.debug("Sizing onto eink-display size: ", im.size)
    im.save(filename, "PNG")


def main():
    logging.info("Accessing API of xkcd")
    xkcd_get_img()





if __name__ == "__main__":
    main()