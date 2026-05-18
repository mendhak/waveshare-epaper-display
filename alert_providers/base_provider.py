import os
from abc import ABC, abstractmethod
import xml.etree.ElementTree as ET
import requests


class BaseAlertProvider(ABC):

    @abstractmethod
    def get_alert(self):
        """
        Implement this method.
        Return a string containing the alert message
        "Yellow warning of wind..."
        """
        pass

    def get_response_json(self, url, headers={}):
        """
        Perform an HTTP GET for a `url` with optional `headers`.
        Returns the response as JSON
        """
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_response_xml(self, url, headers={}):
        """
        Perform an HTTP GET for a `url` with optional `headers`.
        Returns the response as an XML ElementTree
        """
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return ET.fromstring(response.text)


