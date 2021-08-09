from alert_providers.base_provider import BaseAlertProvider
import logging
import xml.etree.ElementTree as ET

class MetOfficeRssFeed(BaseAlertProvider):
    def __init__(self, feed_url):
        self.feed_url = feed_url


    def get_alert(self):
        severe = self.get_response_xml(self.feed_url)
        logging.info(severe)
        root = ET.fromstring(severe)
        for type_tag in root.findall('channel/item'):
            value = type_tag.findtext("title")
            return value
        return ""
