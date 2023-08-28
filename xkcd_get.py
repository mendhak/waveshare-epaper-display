import requests
import json




def xkcd_get_img():
    response = requests.get("https://xkcd.com/info.0.json")
    result = response.json()

    return result["img"]




