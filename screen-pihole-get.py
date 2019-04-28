#!/usr/bin/python

import json
import requests
from xml.dom import minidom
import datetime
import codecs
import os.path
import time
import sys
import os
import html

pihole_address=os.getenv("PIHOLE_ADDR","")

if pihole_address=="":
    print("PIHOLE_ADDR is missing")
    sys.exit(1)


template = 'screen-output-weather.svg'


url= "http://" + pihole_address + "/admin/api.php" 
pihole_json = requests.get(url).json()



ads_blocked = pihole_json['ads_blocked_today']
dns_queries = pihole_json['dns_queries_today']
print("Pihole stats")
print(ads_blocked, dns_queries)

# Process the SVG
output = codecs.open(template , 'r', encoding='utf-8').read()
#output = output.replace('ICON_ONE',icon_dict[icon_one])
output = output.replace('PIHOLE_ADS_BLOCKED', str(ads_blocked) + " blocked")
output = output.replace('PIHOLE_DNS_QUERIES', str(dns_queries) + " queries")
codecs.open('screen-output-weather.svg', 'w', encoding='utf-8').write(output)


