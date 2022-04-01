import os
from abc import ABC, abstractmethod
from utility import get_xml_from_url, get_json_from_url


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
    
    def get_response_json(self, url, headers={}):
        """
        Perform an HTTP GET for a `url` with optional `headers`.
        Caches the response in `cache_file_name` for ALERT_TTL seconds.
        Returns the response as JSON
        """
        return get_json_from_url(url, headers, "cache_severe_alert.json", self.ttl)

    def get_response_xml(self, url, headers={}):
        """
        Perform an HTTP GET for a `url` with optional `headers`.
        Caches the response in `cache_file_name` for ALERT_TTL seconds.
        Returns the response as an XML ElementTree
        """        
        return get_xml_from_url(url, headers, "cache_severe_alert.xml", self.ttl)


    