import os
from abc import ABC, abstractmethod
from utility import is_stale
import logging
import json
import requests


class BaseAlertProvider(ABC):

    ttl = float(os.getenv("ALERT_TTL", 1 * 60 * 60))

    @abstractmethod
    def get_alert(self):
        """
        Implement this method.
        Return a string containing the alert message
        "Yellow warning of wind..."
        """
        pass
    

    def get_response_xml(self, url, headers={}, cache_file_name="severe-alert-cache.xml"):

        logging.info(url)

        if (is_stale(cache_file_name, 300)):
            logging.info("Cache file is stale. Fetching from source.")
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                response_data = response.text

                with open(cache_file_name, 'w') as text_file:
                    text_file.write(response_data)
            except Exception as error:
                logging.error(error)
                logging.error(response.text)
                logging.error(response.headers)
                raise
        else:
            logging.info("Found in cache.")
            with open(cache_file_name, 'r') as file:
                return file.read()
        return response_data


    