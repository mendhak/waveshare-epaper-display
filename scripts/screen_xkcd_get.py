import requests
import logging
import os
import sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.utility import is_stale, configure_logging


configure_logging()

def xkcd_get_img():
    xkcd_file_name = "data/screen_xkcd_comic_strip.png"
    if not is_stale(xkcd_file_name, 3600):
        logging.info("data/screen_xkcd_comic_strip.png is still fresh. Skipping download.")
        sys.exit(1)

    logging.info("Downloading xkcd-json")
    response = requests.get("https://xkcd.com/info.0.json")
    result = response.json()

    logging.info("Downloading xkcd_img")
    logging.info(result["img"])

    project_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = project_root_dir + '/' + xkcd_file_name
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
