import requests
import json
import wget
import logging
import os
import numpy as np
from PIL import Image
from utility import is_stale, configure_logging

configure_logging()

def xkcd_get_img():
    xkcd_file_name = "xkcd-comic-strip.png"
    if not is_stale(xkcd_file_name, 3600):
        logging.info("xkcd-comic-strip.png is still fresh. Skipping download.")
        return

    logging.info("Downloading xkcd-json")
    response = requests.get("https://xkcd.com/info.0.json")
    result = response.json()

    logging.info("Downloading xkcd_img")
    logging.info(result["img"])

    path = os.path.dirname(os.path.realpath(__file__))
    filename = path + '/' + os.path.basename(xkcd_file_name)
    if os.path.exists(filename):
        os.remove(filename)
    wget.download(result["img"], filename)

    # Convert grayscale to pseudo-rgb since grayscale confuses the eink display

    image = np.array(Image.open(filename).convert('RGB'))
    Image.fromarray(image).save(xkcd_file_name)

    """ If the downloaded image is too big to fit into the display downscale it
    while taking the scales into account.
    Afterwards resize the image to fit the screen. Sligh disortions can happen """

    im = Image.open(filename)
    logging.debug("PNG size: ",im.size)

    width = int(os.environ.get('WAVESHARE_WIDTH'))
    height = int(os.environ.get('WAVESHARE_HEIGHT'))
    print(width, height)
    if (im.size[0] > width and im.size[1] > height):
        logging.debug("Picture is bigger than eink-display")
        print("After using thumbnail: ",im.size)
        im.thumbnail((width,height))

    if (im.size[0] < width and im.size[1] < height):
        im = im.resize((width,height))
        logging.debug("Sizing onto eink-display size: ", im.size)
    im.save(filename, "PNG")


def main():
    xkcd_get_img()


if __name__ == "__main__":
    main()
