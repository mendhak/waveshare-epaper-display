from alert_providers.base_provider import BaseAlertProvider
import logging
import xml.etree.ElementTree as ET

class MetOfficeRssFeed(BaseAlertProvider):
    def __init__(self):
        pass

    def get_alert(self):
        # http://www.metoffice.gov.uk/public/data/PWSCache/WarningsRSS/Region/se
        severe = self.get_response_xml("https://www.metoffice.gov.uk/public/data/PWSCache/WarningsRSS/Region/se", cache_file_name="severe.xml")
        logging.info(severe)
        root = ET.fromstring(severe)
        for type_tag in root.findall('channel/item'):
            value = type_tag.findtext("title")
            return value


