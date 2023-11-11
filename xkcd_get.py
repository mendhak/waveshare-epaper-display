import requests
import logging
import os
from PIL import Image
from utility import is_stale, configure_logging
import sys

configure_logging()

def xkcd_get_img():
    xkcd_file_name = "xkcd-comic-strip.png"
    if not is_stale(xkcd_file_name, 3600):
        logging.info("xkcd-comic-strip.png is still fresh. Skipping download.")
        sys.exit(1)

    logging.info("Downloading xkcd-json")
    response = requests.get("https://xkcd.com/info.0.json")
    result = response.json()

    logging.info("Downloading xkcd_img")
    logging.info(result["img"])

    path = os.path.dirname(os.path.realpath(__file__))
    filename = path + '/' + os.path.basename(xkcd_file_name)
    if os.path.exists(filename):
        os.remove(filename)
    image_response = requests.get(result["img"])
    open(filename, 'wb').write(image_response.content)

    logging.info("Resizing the image to fit the screen. Disortions can happen.")

    im = Image.open(filename)
    logging.debug("PNG size: ",im.size)

    width = int(os.environ.get('WAVESHARE_WIDTH'))
    height = int(os.environ.get('WAVESHARE_HEIGHT'))
    im = im.resize((width,height))
    im.save(filename, "PNG")


def main():
    xkcd_get_img()


if __name__ == "__main__":
    main()
